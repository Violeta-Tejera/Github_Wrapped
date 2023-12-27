from github import Github
from utils.github_helpers import get_github_languages
from datetime import datetime, timedelta
from collections import defaultdict

# To Do: Convert this into a class and store values fetched several times in an attribute initialized in the constructor. DRY!!!

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

def get_contributed_repos(github_instance: Github, year: int, showPrivate=False):
    """
    Returns a list of the repos contributed to by a user in a certain year.
    """
    user = github_instance.get_user()
    repos = user.get_repos()
    start = datetime(year, 1, 1, 0, 0, 0)
    end = datetime(year+1, 1, 1, 0, 0, 0)

    repositories_return = []

    for repo in repos:
        # Count commits
        if (repo.visibility == "private" and showPrivate == True) or repo.visibility == "public":
            commits = repo.get_commits(author=user, since=start, until=end).totalCount
            if commits > 0:
                repositories_return.append(repo)

    return repositories_return

def get_languages_user(github_instance: Github, year: int, showPrivate = False):                                     # To do: Reduce time
    """
    Returns a dictionary that maps every language (with at least 1 line of code) with the 
    quantity of lines of code written on year "year" by user "username".
    """
    user = github_instance.get_user()
    repos = user.get_repos()
    try:
        github_languages = get_github_languages()
    except:
        print("Error: Unable to get languages. Aborting now")

    language_stats = defaultdict(int)

    date_since = datetime(year, 1, 1, 0, 0, 0)
    date_until = datetime(year + 1, 1, 1, 0, 0, 0)

    for repo in repos:
        for commit in repo.get_commits(since=date_since, until=date_until, author=user):
            for file in commit.files:
                if (repo.visibility == "private" and showPrivate == True) or repo.visibility == "public":
                    extension = '.' + file.filename.split('.')[-1]
                    language = github_languages.get(extension, 'Unknown')
                    language_stats[language] += file.changes

    return dict(sorted(language_stats.items(), key=lambda x:x[1], reverse=True))

def get_commit_data(github_instance: Github, year: int):
    user = github_instance.get_user()
    repos = user.get_repos()
    start = datetime(year, 1, 1, 0, 0, 0)
    end = datetime(year+1, 1, 1, 0, 0, 0)

    total_count = 0
    public_count = 0

    commit_dates = set()

    for repo in repos:
        #if repo.pushed_at.year >= year and repo.created_at.year <= year:
        commits = repo.get_commits(author=user, since=start, until=end)

        for c in commits:
            commit_dates.add(c.commit.author.date.date())

        count = 0
        for c in commits:
            count += 1

        # Count commits
        total_count += count
        if repo.private == False:
            # Count public commits
            public_count += count

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

    commit_data = {
        "commit_total_count" : total_count,
        "commit_public_count" : public_count,
        "days_with_commits_count" : len(commit_dates),
        "streak_start_date" : streak_start_date,
        "streak_end_date" : streak_end_date,
        "streak_duration" : streak_duration
    }

    return commit_data

def get_statistics_user(github_instance: Github, username, year):
    pass
