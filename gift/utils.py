import os
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
headers = {'Authorization': f"token {GITHUB_TOKEN}",
           'Accept': 'application/vnd.github.v3+json'}


def getRepos(reponame, place, page):
    if place == 'repo':
        url = f'https://api.github.com/search/repositories?q={reponame}+in:name&type=Repositories&page={page}&per_page=60&sort=stars&order=desc'
    elif place == 'readme':
        url = f'https://api.github.com/search/repositories?q={reponame}+in:readme&type=Repositories&page={page}&per_page=60&sort=stars&order=desc'
    else:  # place == description
        url = f'https://api.github.com/search/repositories?q={reponame}+in:description&type=Repositories&page={page}&per_page=60&sort=stars&order=desc'
    try:
        json_resp = requests.get(url, headers=headers)
        # print('headers', json_resp.headers)
        # print('links', json_resp.links)
        # json_resp -> python dictionary
        resp = json_resp.json()
    except:
        resp = {
            'error': 'Sorry, there was a problem with this request. Try again later.'}

    return (json_resp, resp)


def getUsers(username, place, page):
    if place == 'name':
        url = f'https://api.github.com/search/users?q={username}+in:fullname&type=Users&page={page}&per_page=60'
    else:  # place == 'login
        url = f'https://api.github.com/search/users?q={username}+in:login&type=Users&page={page}&per_page=60'
    try:
        json_resp = requests.get(url, headers=headers)
        # json_resp -> python dictionary
        resp = json_resp.json()
    except:
        resp = {
            'error': 'Sorry, there was a problem with this request. Try again later.'}

    return (json_resp, resp)


def getGitUser(username):
    url = f'https://api.github.com/users/{username}'
    try:
        json_resp = requests.get(url, headers=headers)
        # json_resp -> python dictionary
        resp = json_resp.json()
    except:
        resp = {
            'error': 'Sorry, there was a problem with this request. Try again later.'}
    print('resp', resp)
    return resp


def getUserRepos(username, page):
    url = f'https://api.github.com/users/{username}/repos?page={page}&per_page=10'
    try:
        json_resp = requests.get(url, headers=headers)
        # json_resp -> python dictionary
        resp = json_resp.json()
    except:
        resp = {
            'error': 'Sorry, there was a problem with this request. Try again later.'}

    return (json_resp, resp)


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


def buildPaging(links, current_page):
    has_previous, has_other_pages, has_next = False, False, False
    # print('links', links)
    paging = {}
    if links:
        for key in links:
            page = int(parse_qs(urlparse(links[key]['url'])[4])['page'][0])
            paging[key] = page
        # if current_page < 1:
        #     current_page = 1
        # if current_page > paging['last']:
        #     current_page = paging['last']
        if 'next' in paging:
            has_next = True
        if 'next' in links or 'prev' in links:
            has_other_pages = True
        if 'prev' in paging:
            has_previous = True
        paging['has_previous'] = has_previous
        paging['has_other_pages'] = has_other_pages
        paging['has_next'] = has_next
        paging['current'] = current_page
        if not has_next:
            paging['last_page'] = paging['prev'] + 1
        else:
            paging['last_page'] = paging['last']

    return paging
