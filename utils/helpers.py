from github import Github, Auth
import json

def connect(token:str):
    """
    Autentifies with the Github API using the token
    """
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        
        username = g.get_user()
        print(f"You have been connected to Github as user {username.login}")
        return g
    except Exception as e:
        print(f"Error autentifying Github: {e}")
        return None

def disconnect(github:Github):
    """
    Closes github connection
    """
    if github:
        print("Disconnecting")
        github.close()

def load_json(filepath:str):
    """
    Returns, if successful, a Python object containing a decoded JSON document
    """
    try:
        with open(filepath, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Error: Unable to find path in {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode the content of file in {filepath}")
        return None