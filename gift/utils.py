import os
import requests
from datetime import datetime

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


# see: https://stackabuse.com/converting-strings-to-datetime-in-python/
def formatRep(rep_object):
    for rep in rep_object:
        created_str = rep['created_at'].replace('T', ' ')
        created_str = created_str.replace('Z', '')
        created_at = datetime.strptime(
            created_str, "%Y-%m-%d %H:%M:%S")
        rep['created_at'] = created_at

        updated_str = rep['updated_at'].replace('T', ' ')
        updated_str = updated_str.replace('Z', '')
        updated_at = datetime.strptime(
            updated_str, "%Y-%m-%d %H:%M:%S")
        rep['updated_at'] = updated_at

        cropped_name = rep['name'][0:15]
        new_name = cropped_name + ' '
        rep['name'] = new_name
    return rep_object
