"""
Module: user_data_handler

This module provides a UserData class for handling GitHub user data and related functionalities.

Classes:
    UserData: A class for managing GitHub user data, repositories, commits, and more.

Methods:
    - __init__: Initializes an instance of the UserData class.
    - get_created_repos: Returns a list of repositories created by the user in a certain year.
    - get_contributed_repos: Returns a list of repositories contributed to by the user in a
    certain year.
    - get_languages_user: Returns language statistics for the user's contributions.
    - get_commit_data: Returns data related to the user's commit history.

Example:
    # Creating an instance of UserData
    github_instance = Github("your_username", "your_token")
    user_data = UserData(
        github_instance=github_instance,
        username="your_username",
        year=2023,
        show_private=True,
        show_repo_info=True
    )

    # Getting commit data for the user
    commit_data = user_data.get_commit_data()

    # Getting language statistics for the user's contributions
    language_stats = user_data.get_languages_user()

    # Getting repositories created by the user in a certain year
    created_repos = user_data.get_created_repos()

    # Getting repositories contributed to by the user in a certain year
    contributed_repos = user_data.get_contributed_repos()

"""

from github import Github
from utils.github_helpers import get_language
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


class UserData:
    """
    Class to store the data from the users
    """

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
        """
        Getter for github_instance
        """
        return self.__github_instance

    @github_instance.setter
    def github_instance(self, value):
        """
        Setter for github_instance
        """
        self.__github_instance = value

    @property
    def show_repo_info(self):
        """
        Getter for show_repo_info
        """
        return self.__show_repo_info

    @show_repo_info.setter
    def show_repo_info(self, value):
        """
        Setter for show_repo_info
        """
        self.__show_repo_info = value

    @property
    def username(self):
        """
        Getter for username
        """
        return self.__username

    @username.setter
    def username(self, value):
        """
        Setter for username
        """
        self.__username = value

    @property
    def year(self):
        """
        Getter for year
        """
        return self.__year

    @year.setter
    def year(self, value):
        """
        Setter for year
        """
        self.__year = value

    @property
    def show_private(self):
        """
        Getter for show_private
        """
        return self.__show_private

    @show_private.setter
    def show_private(self, value):
        """
        Setter for show_private
        """
        self.__show_private = value

    @property
    def user(self):
        """
        Getter for user
        """
        return self.__user

    @user.setter
    def user(self, value):
        """
        Setter for user
        """
        self.__user = value

    @property
    def commit_years(self):
        """
        Getter for commit_years
        """
        return self.__commit_years

    @commit_years.setter
    def commit_years(self, value):
        """
        Setter for commit_years
        """
        self.__commit_years = value

    @property
    def total_count(self):
        """
        Getter for total_count
        """
        return self.__total_count

    @total_count.setter
    def total_count(self, value):
        """
        Setter for total_count
        """
        self.__total_count = value

    @property
    def public_count(self):
        """
        Getter for public_count
        """
        return self.__public_count

    @public_count.setter
    def public_count(self, value):
        """
        Setter for public_count
        """
        self.__public_count = value

    @property
    def repo_commit(self):
        """
        Getter for repo_commit
        """
        return self.__repo_commit

    @repo_commit.setter
    def repo_commit(self, value):
        """
        Setter for repo_commit
        """
        self.__repo_commit = value

    @property
    def user_repos(self):
        """
        Getter for user_repos
        """
        return self.__user_repos

    @user_repos.setter
    def user_repos(self, value):
        """
        Setter for user_repos
        """
        self.__user_repos = value

    def __get_commit_years_basic_data(self):
        """
        Gets basic data related to commits, such as the total count (and public total count)
        of commits of the year; and several data related to each repository

        Note:
            - Method is private
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

        Returns:
            list: repos created by a user in a certain year
        """
        repos = [r for r in self.user_repos if r.fork is False and r.created_at.year ==
                 self.year and r.owner == self.github_instance.get_user(self.username)]

        return repos

    def get_contributed_repos(self):
        """
        Returns a list of the repos contributed to by a
        user in a certain year.

        Returns:
            list: Repos contributed to by a user in a certain year
        """
        repositories_return = []

        for repo in self.user_repos:
            # Count commits
            if self.repo_commit[repo]["total_count_author"] > 0:
                repositories_return.append(repo)

        return repositories_return

    def get_languages_user(self):
        language_stats = defaultdict(int)

        def process_commit(commit):
            for file in commit.files:
                extension = '.' + file.filename.split('.')[-1]
                language = get_language(extension, "languages_extensions.db")
                language_stats[language] += file.changes

        with ThreadPoolExecutor() as executor:
            futures = []
            for repo in self.get_contributed_repos():
                for commit in self.repo_commit[repo]["commits_repo_author"]:
                    if (repo.visibility ==
                            "private" and self.show_private) or repo.visibility == "public":
                        futures.append(
                            executor.submit(
                                process_commit,
                                commit,
                                repo.visibility))

            # Wait for all futures to complete
            for future in futures:
                future.result()

        return dict(sorted(language_stats.items(),
                    key=lambda x: x[1], reverse=True))

    def get_commit_data(self):
        """
        Returns some commit dates data related to the longest commit streak duration, start and
        ending dates; and the total days with commits of the year

        Returns:
            dict: Dictionary with commit data
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
