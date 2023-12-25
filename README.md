
# Github Wrapped 
[@Violeta-Tejera](https://www.github.com/Violeta-Tejera)

<p align="center">
  <img src="https://github.com/Violeta-Tejera/Github_Wrapped/assets/80209320/200beba1-f3d2-4995-8693-455e83f574aa" width="200" height="200">
</p>

The purpose of this project is to develop a tool that offers Github users a comparable experience to Spotify Wrapped, an annual viral marketing campaign made by Spotify since 2016, in which their users are shown several statistics about their music tendencies during the current year.

## Disclaimer

This software is provided to you "as is", and you use it at your own risk. Under no circumstances shall any author be liable for direct, indirect, special, indicental or consequential damages resulting from the use, miuse, or inability to use this software, even if the authors have been advised of the possibility of such damages.

## Features

- **Language statistics**: Discover the variety of programming languages you've used during the past year.
- **Top language**: Find out which programming language dominated your contributions.
- **Repository insights**: Which are the repositories you've created and/or contributed to during this last year? What can be told about them?

## Roadmap
- Social engagement statistics (stars, followers,...)
- Commit history (streaks, activity,...)
- More statistics...
- GUI

## Documentation

- Python Official documentation: https://docs.python.org/3/
- Github Rest API documentation: https://docs.github.com/es/rest?apiVersion=2022-11-28
- PyGithub documentation: https://pygithub.readthedocs.io/en/latest/introduction.html

## Running it locally

1. **Clone the repository:**
  ```bash
  git clone https://github.com/Violeta-Tejera/Github_Wrapped
  cd Github_Wrapped
  ```
2. **Install dependencies**
```python
  pip install -r requirements.txt
```

4. **Modify the config.json file to comply with your details:**
   
  -username: Your username goes here
  
  -token: Your personal access token goes here. More info. on that here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
 
  -year: Type in the year you want to view
  
  -showPrivate: Some functionalities toggle between public repositories and all repositories. Choose true for the latter.

  -showRepoInfo: This boolean let's you choose whether or not you'd like to show extra information about the displayed repos, such as the quantity of commits it had during the year, or the number of new stargazers it had. 

6. **Run**
```python
python githubwrapped.py
```


## Contact info

Should you have any further inquiry of would like to provide your feedback, please do reach out to me via email at vtejmun@gmail.com


