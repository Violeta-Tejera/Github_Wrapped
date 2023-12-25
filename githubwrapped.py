from utils.helpers import *
from api.repo import *
from api.user import *

def repositories_details(github, username, year, showPrivate):
    print("------------------------------------------------")
    print("Repositories and code")
    print("------------------------------------------------")
    repos = get_created_repos(github, username, year, showPrivate=showPrivate)
    print("Repositories created this year: ")
    for r in repos:
        print(r.full_name, " Top Language: ", r.language)      
    print("------------------------------------------------")
    repos = get_contributed_repos(github, username, year)
    print("Repositories contributed to this year: ")
    for r in repos:
        print(r.full_name, " Top Language: ", r.language)  
    print("------------------------------------------------")
    languages = get_languages_user(github, username, year)
    print(f"You coded in more than {len(languages)} languages this year")
    languages_list = list(languages.items())
    if languages_list[0][0] != 'Unknown' or len(languages_list) == 0:
        top_language = languages_list[0]
    else:
        top_language = languages_list[1]
    print(f"But your favourite was without a doubt {top_language[0]}")

def commits_details(github, username, year, showPrivate):
    ### Commits        
    print("Commits")
        
    # Num. of commits of the year
        
    # Max streak of commits (dates)
        
    # Max streak of days without commits (dates)
        
    # Histogram of commits per month

def social_details(github, username, year, showPrivate):
    ### Social
    print("Social")
    # Stars (Given and received)

    # Top 2 collaborators
        
    # Num de nuevos seguidores
        
    # Num de nuevas cuentas seguidas

def main():
    filename = "config.json"
    jsonfile = load_json(filename)

    username = jsonfile.get('username')
    token = jsonfile.get('token')
    year = jsonfile.get('year')
    showPrivate = jsonfile.get('showPrivate')

    github = connect(token)

    if github:
        repositories_details(github, username, year, showPrivate)     
        
    disconnect(github)

main()
