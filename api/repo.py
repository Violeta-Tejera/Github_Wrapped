from github import Github, Repository
from api.user import *
import datetime

# TODO: check & debug
def print_statistics_repo(user: UserData, repo: Repository):       # TODO: toggle with private
    print(f"Showing repository statistics for {repo.full_name} in {user.year}")

    # License
    try:
        license = repo.get_license()
    except:
        print("This repository has no license")
    else:
        print("License: ", license.license.name)

    # Contributors
    contributors = repo.get_contributors()
    print(f"This repository has {contributors.totalCount} contributors:")
    for c in contributors:
        print(f"- {c.login}")

    # Languages
    languages = repo.get_languages().keys()
    print(f"This repository is written in {len(languages)} different languages: ")
    for l in languages:
        print(f"- {l}")
    
    # Downloads
    try:
        downloads = repo.get_downloads()
        downloads_this_year = 0
        for d in downloads: 
            if d.created_at.year == user.year:
                downloads_this_year += 1
    except:
        print("This repository hasn't got any downloads (yet!)")
    else:
        print(f"This repository has had {downloads_this_year} downloads during this year, {user.year}")
    
    # Forks
    forks_this_year = 0
    for f in repo.get_forks(): 
        if f.created_at.year == user.year:
            forks_this_year += 1
    if forks_this_year != 0:
        print(f"This repository has had {forks_this_year} forks during this year, {user.year}")
    
    # Issues
    start_date = datetime.datetime(user.year, 1, 1, 0, 0, 0)
    issues_this_year = [i for i in repo.get_issues(since=start_date) if i.created_at.year == user.year]
    closed = 0
    for i in issues_this_year:
        if i._state == "Closed":
            closed += 1
    if len(issues_this_year) != 0:
        print(f"This repository has had {len(issues_this_year)} issues on {user.year}, of which {closed} where closed")

    # Commits
    commits_this_year = user.repo_commit[repo]["total_count"]
    commits_made_by_user = user.repo_commit[repo]["total_count_author"]
    print(f"This repository has had {len(commits_this_year)} commits on {user.year}, of which {commits_made_by_user} were made by you")
    

    # Stargazers
    stargazers = repo.get_stargazers_with_dates()
    stargazers_this_year = 0
    for stg in stargazers:
        if stg.starred_at.year == user.year:
            stargazers_this_year += 1
    if stargazers.totalCount != 0 or stargazers_this_year != 0:
        print(f"Of {stargazers.totalCount} stars this repository has, {stargazers_this_year} were given this year {user.year}")

    # Releases
    releases_this_year = 0 
    for r in repo.get_releases():
        if r.created_at.year == user.year:
            releases_this_year += 1
    if releases_this_year != 0:
        print(f"This repository has had {releases_this_year} releases this year")




