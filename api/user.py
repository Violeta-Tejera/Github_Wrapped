from github import Github
from utils.github_helpers import get_github_languages
from datetime import datetime, timedelta
from collections import defaultdict

# TODO: Convert this into a class and store values fetched several times in an attribute initialized in the constructor. DRY!!!

class UserData:
    def __init__(self, github_instance: Github, username: str, year: int, showPrivate:bool, showRepoinfo:bool):
        self.github_instance = github_instance
        self.username = username
        self.year = year
        self.showPrivate = showPrivate
        self.user = github_instance.get_user()
        
        if showPrivate == True:
            self.user_repos = self.user.get_repos(visibility='all')
        else:
            self.user_repos = self.user.get_repos(visibility='public')

        self.showRepoInfo = showRepoinfo

        self.commit_years = 0
        self.total_count = 0
        self.public_count = 0
        self.repo_commit = dict()
        commit = self.__get_commit_years_basic_data() 

    # TODO debug
    def __get_commit_years_basic_data(self):
        start = datetime(self.year, 1, 1, 0, 0, 0)
        end = datetime(self.year+1, 1, 1, 0, 0, 0)
        
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
                if c.author.login == self.user.login:
                    commits_repo_author.append(c)
                    author_count += 1

            self.repo_commit[repo] = {
                "total_count": count, 
                "commits_repo_total": commits_repo, 
                "total_count_author": author_count, 
                "commits_repo_author": commits_repo_author
            }
            total_count += author_count

            if repo.private == False:
                public_count += author_count


        self.commit_years = commits_year
        self.total_count = total_count
        self.public_count = public_count

    def get_created_repos(self):
        """
        Returns a list of the repos created by a user in a certain year. You can toggle
        whether or not you want to display the private repositories.
        """
        repos = [r for r in self.user_repos if r.fork is False and r.created_at.year == self.year and r.owner == self.github_instance.get_user(self.username)]

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
    # TODO: Debug. Why is TSQL suddenly the most used language? xd
    def get_languages_user(self):                                     
        """
        Returns a dictionary that maps every language (with at least 1 line of code) with the 
        quantity of lines of code written on year "year" by user "username".
        """
        try:
            github_languages = get_github_languages()
        except:
            print("Error: Unable to get languages. Aborting now")

        language_stats = defaultdict(int)

        for repo in self.user_repos:
            for commit in self.repo_commit[repo]["commits_repo_author"]:
                for file in commit.files:
                    if (repo.visibility == "private" and self.showPrivate == True) or repo.visibility == "public":
                        extension = '.' + file.filename.split('.')[-1]
                        language = github_languages.get(extension, 'Unknown')
                        language_stats[language] += file.changes
        
        print(language_stats)
        return dict(sorted(language_stats.items(), key=lambda x:x[1], reverse=True))

    def get_commit_data(self):

        commit_dates = set()

        for repo in self.user_repos:
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
            if commit_dates[i] - commit_dates[i-1] == timedelta(days=1):
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

        streak_start_date += timedelta(days=1)
        streak_duration -= 1

        commit_data = {
            "days_with_commits_count" : len(commit_dates),
            "streak_start_date" : streak_start_date,
            "streak_end_date" : streak_end_date,
            "streak_duration" : streak_duration
        }

        return commit_data

