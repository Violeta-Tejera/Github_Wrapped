from github import Github
from utils.github_helpers import get_github_languages
from datetime import datetime, timedelta
from collections import defaultdict

# TODO: Convert this into a class and store values fetched several times
# in an attribute initialized in the constructor. DRY!!!


class UserData:
    def __init__(
            self,
            github_instance: Github,
            username: str,
            year: int,
            show_private: bool,
            show_repo_info: bool):
        self.__github_instance = github_instance
        self.__username = username
        self.__year = year
        self.__show_private = show_private
        self.__user = github_instance.get_user()

        if show_private:
            self.__user_repos = self.user.get_repos(visibility='all')
        else:
            self.__user_repos = self.user.get_repos(visibility='public')

        self.__show_repo_info = show_repo_info

        self.__commit_years = 0
        self.__total_count = 0
        self.__public_count = 0
        self.__repo_commit = {}
        self.__get_commit_years_basic_data()

    @property
    def github_instance(self):
        return self.__github_instance

    @github_instance.setter
    def github_instance(self, value):
        self.__github_instance = value

    @property
    def show_repo_info(self):
        return self.__show_repo_info

    @show_repo_info.setter
    def show_repo_info(self, value):
        self.__show_repo_info = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    @property
    def show_private(self):
        return self.__show_private

    @show_private.setter
    def show_private(self, value):
        self.__show_private = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def commit_years(self):
        return self.__commit_years

    @commit_years.setter
    def commit_years(self, value):
        self.__commit_years = value

    @property
    def total_count(self):
        return self.__total_count

    @total_count.setter
    def total_count(self, value):
        self.__total_count = value

    @property
    def public_count(self):
        return self.__public_count

    @public_count.setter
    def public_count(self, value):
        self.__public_count = value

    @property
    def repo_commit(self):
        return self.__repo_commit

    @repo_commit.setter
    def repo_commit(self, value):
        self.__repo_commit = value

    @property
    def user_repos(self):
        return self.__user_repos

    @user_repos.setter
    def user_repos(self, value):
        self.__user_repos = value

    def __get_commit_years_basic_data(self):
        """
        Gets basic data related to commits, such as the total count (and public total count)
        of commits of the year; and several data related to each repository
        """
        start = datetime(self.year, 1, 1, 0, 0, 0)
        end = datetime(self.year + 1, 1, 1, 0, 0, 0)

        commits_year = []
        total_count = 0
        public_count = 0

        for repo in self.user_repos:
            commits_repo = repo.get_commits(since=start, until=end)
            count = 0
            author_count = 0
            commits_repo_author = []
            for c in commits_repo:
                count += 1
                if c.author and c.author.login == self.user.login:
                    commits_repo_author.append(c)
                    author_count += 1

            self.repo_commit[repo] = {
                "total_count": count,
                "commits_repo_total": commits_repo,
                "total_count_author": author_count,
                "commits_repo_author": commits_repo_author
            }

            total_count += author_count

            if not repo.private:
                public_count += author_count

        self.commit_years = commits_year
        self.total_count = total_count
        self.public_count = public_count

    def get_created_repos(self):
        """
        Returns a list of the repos created by a user in a certain year. You can toggle
        whether or not you want to display the private repositories.
        """
        repos = [r for r in self.user_repos if r.fork is False and r.created_at.year ==
                 self.year and r.owner == self.github_instance.get_user(self.username)]

        return repos

    def get_contributed_repos(self):
        """
        Returns a list of the repos contributed to by a user in a certain year.
        """
        repositories_return = []

        for repo in self.user_repos:
            # Count commits
            if self.repo_commit[repo]["total_count_author"] > 0:
                repositories_return.append(repo)

        return repositories_return

    # TODO: SQLITE3 DB for get_github_languages() functionalities
    # TODO: Reduce time
    def get_languages_user(self):
        """
        Returns a dictionary that maps every language (with at least 1 line of code) with the
        quantity of lines of code written on year "year" by user "username".
        """
        try:
            github_languages = get_github_languages()
        except BaseException:
            print("Error: Unable to get languages. Aborting now")

        language_stats = defaultdict(int)

        for repo in self.get_contributed_repos():
            for commit in self.repo_commit[repo]["commits_repo_author"]:
                for file in commit.files:
                    if (repo.visibility ==
                            "private" and self.show_private) or repo.visibility == "public":
                        extension = '.' + file.filename.split('.')[-1]
                        language = github_languages.get(extension, 'Unknown')
                        language_stats[language] += file.changes

        return dict(
            sorted(
                language_stats.items(),
                key=lambda x: x[1],
                reverse=True))

    def get_commit_data(self):
        """
        Returns some commit dates data related to the longest commit streak duration, start and
        ending dates; and the total days with commits of the year
        """

        commit_dates = set()

        for repo in self.get_contributed_repos():
            commits = self.repo_commit[repo]["commits_repo_author"]
            for c in commits:
                commit_dates.add(c.commit.author.date.date())

        commit_dates = sorted(commit_dates)

        streak_start_date = None
        streak_end_date = None
        streak_duration = 0
        current_start = None
        current_end = None
        current_streak_duration = 0

        for i in range(1, len(commit_dates)):
            if commit_dates[i] - commit_dates[i - 1] == timedelta(days=1):
                current_streak_duration += 1
                current_end = commit_dates[i]
            else:
                if current_streak_duration > streak_duration:
                    streak_duration = current_streak_duration
                    streak_start_date = current_start
                    streak_end_date = current_end

                current_start = commit_dates[i]
                current_end = commit_dates[i]
                current_streak_duration = 1

        if current_streak_duration > streak_duration:
            streak_start_date = current_start
            streak_end_date = current_end
            streak_duration = current_streak_duration

        if streak_start_date:
            streak_start_date += timedelta(days=1)
            streak_duration -= 1

        commit_data = {
            "days_with_commits_count": len(commit_dates),
            "streak_start_date": streak_start_date,
            "streak_end_date": streak_end_date,
            "streak_duration": streak_duration
        }

        return commit_data
