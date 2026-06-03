import requests

def fetch_repo(owner, repo_name):

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo_name}"
    )

    response = requests.get(url)

    if response.status_code != 200:

        return None

    return response.json()