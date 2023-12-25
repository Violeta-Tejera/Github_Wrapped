from github import Github, Repository
from utils.github_helpers import get_github_languages
from datetime import datetime
from collections import defaultdict

def get_created_repos(github_instance: Github, username: str, year: int, showPrivate=False):
    """
    Returns a list of the repos created by a user in a certain year. You can toggle
    whether or not you want to display the private repositories.
    """
    
    if showPrivate == True:
        user = github_instance.get_user() # authenticated user can get private repos too
        user_repos = user.get_repos(visibility='all')
    else:
        user = github_instance.get_user(username)
        user_repos = user.get_repos()

    repos = [r for r in user_repos if r.fork is False and r.created_at.year == year and r.owner == github_instance.get_user(username)]

    return repos

def get_contributed_repos(github_instance: Github, username: str, year: int):
    """
    Returns a list of the repos contributed to by a user in a certain year.
    """

    user = github_instance.get_user(username)
    repos = []

    repos += get_created_repos(github_instance, username, year)

    for event in user.get_events():
        if event.type == "PushEvent" and event.created_at.year == year:
            repo = event.repo 
            if repo not in repos:
                repos.append(repo)

    return repos

def get_languages_user(github_instance: Github, username: str, year: int, showPrivate=False):
    """
    Returns a dictionary that maps every language (with at least 1 line of code) with the 
    quantity of lines of code written on year "year" by user "username".
    """
    user = github_instance.get_user(username)
    try:
        github_languages = get_github_languages()
    except:
        print("Error: Unable to get languages. Aborting now")

    language_stats = defaultdict(int)

    date_since = datetime(year, 1, 1, 0, 0, 0)
    date_until = datetime(year + 1, 1, 1, 0, 0, 0)

    for repo in user.get_repos():
        for commit in repo.get_commits(since=date_since, until=date_until, author=user):
            for file in commit.files:
                extension = '.' + file.filename.split('.')[-1]
                language = github_languages.get(extension, 'Unknown')
                language_stats[language] += file.changes

    return dict(sorted(language_stats.items(), key=lambda x:x[1], reverse=True))

def get_statistics_user(github_instance: Github, username, year):
    pass
