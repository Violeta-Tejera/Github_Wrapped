from collections import defaultdict
import requests
import yaml
import os.path
import sqlite3

def github_languages_db(filepath):
    """
    Returns a dictionary that maps each extension to the name of a language known to Github.
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
            if isinstance(extensions, str):
                extensions_list = extensions.split()
            elif isinstance(extensions, list):
                extensions_list = extensions

            for extension in extensions_list:
                cursor.execute("INSERT OR REPLACE INTO language_mapping (extension, language) VALUES (?, ?)", (extension, lang))

def get_language(extension, filepath):
    if not os.path.isfile(filepath):
        github_languages_db(filepath)

    with sqlite3.connect(filepath) as db:
        cursor = db.cursor()
        cursor.execute("SELECT language FROM language_mapping WHERE extension = ?", (extension,))
        result = cursor.fetchone()

    return result[0] if result else None
