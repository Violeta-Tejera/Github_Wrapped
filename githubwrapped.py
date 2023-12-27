from utils.helpers import *
from api.repo import *
from api.user import *

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
        if user.showRepoInfo:
            print_statistics_repo(user, r)  
            print("\n")
    print("\n------------------------------------------------\n")

    # Repositories contributed to this year
    repos = user.get_contributed_repos()
    print("Repositories contributed to this year: ")
    for r in repos:
        print(r.full_name, " Top Language: ", r.language)  
        # Extra info.
        if user.showRepoInfo == True:
            print_statistics_repo(user, r)  
            print("\n")
    print("\n------------------------------------------------\n")

    # Languages top and count
    #languages = user.get_languages_user()
    #print(f"You coded in more than {len(languages)} languages this year")
    #languages_list = list(languages.items())
    #if languages_list[0] != 'Unknown' or len(languages_list) == 0:
    #    top_language = languages_list[0]
    #else:
    #    top_language = languages_list[1]
    #print(f"But your favourite was without a doubt {top_language[0]}")
    

# TODO finish
def commits_details(user: UserData):
    """
    Displays info. related to commits made by the user
    """
    ### Commits        
    print("Commits")
    data = user.get_commit_data()

    # Num. of commits of the year
    print("You made", user.total_count, "commits this year, of which", user.public_count, "were public contributions")

    # Max streak of commits (dates) TODO

    # Histogram of commits per month    TODO

# TODO
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
    showRepoinfo = jsonfile.get("showRepoInfo")

    github = connect(token)
    user = UserData(github, username, year, showPrivate, showRepoinfo)

    # TODO debug showPrivate, public repos from other users/organizations are not being shown, might be related to github.get_user(), dunno 

    if github:
        repositories_details(user)     
        commits_details(user)
        
    disconnect(github)

main()
