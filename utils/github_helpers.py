"""
Module: github_languages

This module provides functions to work with GitHub programming language data, 
specifically related to file extensions and their corresponding 
programming languages.

Functions:
    - github_languages_db(filepath): Returns a dictionary that maps each extension to the name of a 
    language known to GitHub.
    - get_language(extension: str, filepath: str) -> str: Fetches the language corresponding to a 
    certain extension in the database corresponding to the filepath. If the database is not present 
    in that filepath, it will create the language database with github_languages_db.

Dependencies:
    - requests: Used for making HTTP requests to fetch GitHub language data.
    - yaml: Used for parsing YAML data.
    - os.path: Used for checking if a file exists at a given filepath.
    - sqlite3: Used for SQLite database operations.
"""

import requests
import yaml
import os.path
import sqlite3


def github_languages_db(filepath):
    """
    Returns a dictionary that maps each extension to the name of a 
    language known to Github.

    Args:
        filepath (string): Filepath to database
    """
    url = 'https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
    else:
        raise Exception("Unable to get github languages info")

    github_languages = yaml.safe_load(data)

    with sqlite3.connect(filepath) as db:
        cursor = db.cursor()

        create_table = """
        CREATE TABLE IF NOT EXISTS language_mapping(
            extension TEXT PRIMARY KEY,
            language TEXT
        )
        """
        cursor.execute(create_table)

        for lang, properties in github_languages.items():
            extensions = properties.get("extensions", "")
            type = properties.get("type", "")

            if type == "programming":
                if isinstance(extensions, str):
                    extensions_list = extensions.split()
                elif isinstance(extensions, list):
                    extensions_list = extensions

                for extension in extensions_list:
                    cursor.execute(
                        "INSERT OR REPLACE INTO language_mapping (extension, language) VALUES (?, ?)", (extension, lang))


def get_language(extension: str, filepath: str) -> str:
    """ Fetchs the language corresponding to a certain extension in the 
    database corresponding to the filepath. If database is not present in 
    that filepath, it will create the language database with github_languages_db

    Args:
        extension (string): File extension
        filepath (string): Filepath to database

    Returns:
        str: Programming language corresponding to the extension
    """
    if not os.path.isfile(filepath):
        github_languages_db(filepath)

    with sqlite3.connect(filepath) as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT language FROM language_mapping WHERE extension = ?", (extension,))
        result = cursor.fetchone()

    return result[0] if result else None
