from collections import defaultdict
import requests
import yaml


def get_github_languages():
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

    extension_mapping = defaultdict(str)

    for language, properties in github_languages.items():
        extensions = properties.get('extensions', '')
        type = properties.get("type", "")

        if type == "programming":
            if isinstance(extensions, str):
                extensions_list = extensions.split()
            elif isinstance(extensions, list):
                extensions_list = extensions

            for extension in extensions_list:
                extension_mapping[extension] = language

    return extension_mapping
