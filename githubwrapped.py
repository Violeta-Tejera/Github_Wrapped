"""
Main script for fetching and displaying various details related to a GitHub user.

Functions:
    - repositories_details: Displays information related to repositories, including those created and contributed to by the user.
    - commits_details: Displays information related to commits made by the user, such as the number of commits, commit streak duration, etc.
    - social_details: Displays social-related information, including stars received, top collaborators, new followers, and new accounts followed.
    - main: Main entry point for the script, which orchestrates the execution of various functions.

Example:
    python githubwrapped.py

Note:
    Make sure to install the required dependencies by running:
    pip install -r requirements.txt
"""

from utils.helpers import load_json, connect, disconnect
from api.RepoData import RepoData
from api.UserData import UserData


def repositories_details(user: UserData):
    """
    Displays info. related to repositories
    """

    print("------------------------------------------------")
    print("Repositories and code")
    print("------------------------------------------------")
    
    # Repositories created this year
    repos = user.get_created_repos()
    print("Repositories created this year: ")
    for r in repos:
        print(r.full_name, " Top Language: ", r.language)
        # Extra info.
        if user.show_repo_info:
            repoData = RepoData(user, r, True)
            repoData.print_statistics_repo()
            print("\n")
    print("\n------------------------------------------------\n")

    # Repositories contributed to this year
    repos = user.get_contributed_repos()
    print("Repositories contributed to this year: ")
    for r in repos:
        print(r.full_name, " Top Language: ", r.language)
        # Extra info.
        if user.show_repo_info:
            repoData = RepoData(user, r, True)
            repoData.print_statistics_repo()
            print("\n")
    print("\n------------------------------------------------\n")
    """
    # Languages top and count
    languages = user.get_languages_user()
    print(f"You coded in more than {len(languages)} languages this year")
    languages_list = list(languages.items())
    if languages_list[0][0] != 'Unknown' or len(languages_list) == 0:
        print("hola")
        top_language = languages_list[0]
    else:
        print("adios")
        top_language = languages_list[1]

    print(languages_list)
    print(top_language)
    print(f"But your favourite was without a doubt {top_language}")
    """


def commits_details(user: UserData):
    """
    Displays info. related to commits made by the user
    """
    # Commits
    print("Commits")
    data = user.get_commit_data()

    # Num. of commits of the year
    print(
        "You made",
        user.total_count,
        "commits this year, of which",
        user.public_count,
        "were public contributions. You commited for",
        data["days_with_commits_count"],
        "days this year!")

    # Max streak of commits (dates)
    print(
        "Your longest commit streak lasted for",
        data["streak_duration"],
        "days, between",
        data["streak_start_date"],
        "and",
        data["streak_end_date"])

    # Histogram of commits per month    TODO

# TODO this function too


def social_details(github, username, year, show_private):
    # Social
    print("Social")
    # Stars (Given and received)

    # Top 2 collaborators

    # Num de nuevos seguidores

    # Num de nuevas cuentas seguidas


def main():
    """
    Main entry point for the script. This script performs all the functionality. 
    """

    filename = "config.json"
    jsonfile = load_json(filename)

    username = jsonfile.get('username')
    token = jsonfile.get('token')
    year = jsonfile.get('year')
    show_private = jsonfile.get('show_private')
    show_repo_info = jsonfile.get("show_repo_info")

    github = connect(token)
    user = UserData(github, username, year, show_private, show_repo_info)

    if github:
        repositories_details(user)
        #commits_details(user)

    disconnect(github)


main()
