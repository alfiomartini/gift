import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
headers = {'Authorization': f"token {GITHUB_TOKEN}",
           'Accept': 'application/vnd.github.v3+json'}


def getGitUser(username):
    url = f'https://api.github.com/users/{username}'
    try:
        json_resp = requests.get(url, headers=headers)
        # json_resp -> python dictionary
        resp = json_resp.json()
    except:
        resp = {
            'error': 'Sorry, there was a problem with this request. Try again later.'}

    return resp


def getUserRepos(username):
    url = f'https://api.github.com/users/{username}/repos'
    try:
        json_resp = requests.get(url, headers=headers)
        # json_resp -> python dictionary
        resp = json_resp.json()
    except:
        resp = {
            'error': 'Sorry, there was a problem with this request. Try again later.'}

    return resp


def format_date():
    pass
