"""
Module: github_connector

This module provides functions for connecting to the GitHub API using a 
token, disconnecting from the GitHub API, and loading JSON data from a file.

Functions:
    - connect(token: str) -> Github: Authenticates with the Github API using 
    the provided token.
    - disconnect(github: Github): Closes the connection to the GitHub API.
    - load_json(filepath: str) -> dict: Returns a Python object containing a 
    decoded JSON document if successful.

Dependencies:
    - github.Github: Used for interacting with the GitHub API.
    - github.Auth: Used for authentication with the GitHub API.
    - json: Used for reading and decoding JSON data from a file.

Usage:
    You can use the functions provided in this module to connect to the 
    GitHub API, disconnect from the API, and load JSON data from a file.

"""


from github import Github, Auth
import json


def connect(token: str):
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


def disconnect(github: Github):
    """
    Closes github connection
    """
    if github:
        print("Disconnecting")
        github.close()


def load_json(filepath: str):
    """
    Returns, if successful, a Python object containing a decoded JSON document
    """
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Error: Unable to find path in {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode the content of file in {filepath}")
        return None
