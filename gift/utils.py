import os
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from .adv_search import config

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
headers = {'Authorization': f"token {GITHUB_TOKEN}",
           'Accept': 'application/vnd.github.v3+json'}


def getRepos(reponame, place, page, sort):
    if config.getConfig('advanced') == True:
        settings = config.getConfigAll()
        created = settings['created']
        updated = settings['updated']
        stars = settings['stars']
        forks = settings['forks']
        # I should think on a list of languages (but it is too big)
        # https://github.com/github/linguist/blob/master/lib/linguist/languages.yml
        if place == 'repo':
            url = f'https://api.github.com/search/repositories?q={reponame}+in:name+stars:>={stars}+forks:>={forks}+pushed:>={updated}&type=Repositories&page={page}&per_page=60&sort={sort}&order=desc'
            print('url', url)
        elif place == 'readme':
            url = f'https://api.github.com/search/repositories?q={reponame}+in:readme+stars:>={stars}+forks:>={forks}+pushed:>={updated}&type=Repositories&page={page}&per_page=60&sort={sort}&order=desc'
            print('url', url)
        else:  # place == description
            url = f'https://api.github.com/search/repositories?q={reponame}+in:description+stars:>={stars}+forks:>={forks}+pushed:>={updated}&type=Repositories&page={page}&per_page=60&sort={sort}&order=desc'
            print('url', url)
    else:
        if place == 'repo':
            url = f'https://api.github.com/search/repositories?q={reponame}+in:name&type=Repositories&page={page}&per_page=60&sort={sort}&order=desc'
        elif place == 'readme':
            url = f'https://api.github.com/search/repositories?q={reponame}+in:readme&type=Repositories&page={page}&per_page=60&sort={sort}&order=desc'
        else:  # place == description
            url = f'https://api.github.com/search/repositories?q={reponame}+in:description&type=Repositories&page={page}&per_page=60&sort={sort}&order=desc'
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


def getUsers(username, place, page, sort):
    if sort == 'best':
        sort = ''
    elif sort == 'repos':
        sort = 'repositories'
    # print('getUser sort', sort)
    if config.getConfig('advanced') == True:
        settings = config.getConfigAll()
        created = settings['created']
        repositories = settings['repositories']
        followers = settings['followers']
        if place == 'name':
            url = f'https://api.github.com/search/users?q={username}+in:fullname+repos:>={repositories}+created:>={created}+followers:>={followers}&type=Users&page={page}&per_page=60&sort={sort}&o=desc'
        else:  # place == 'login
            url = f'https://api.github.com/search/users?q={username}+in:login+repos:>={repositories}+created:>={created}+followers:>={followers}&type=Users&page={page}&per_page=60&sort={sort}&o=desc'
    else:
        if place == 'name':
            url = f'https://api.github.com/search/users?q={username}+in:fullname&type=Users&page={page}&per_page=60&sort={sort}&o=desc'
        else:  # place == 'login
            url = f'https://api.github.com/search/users?q={username}+in:login&type=Users&page={page}&per_page=60&sort={sort}&o=desc'
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
        # {
        # "message": "Not Found",
        # "documentation_url": "https://docs.github.com/rest/reference/users#get-a-user"
        # }
        resp = json_resp.json()
    except:
        resp = {
            'error': 'Sorry, there was a problem with this request. Try again later.'}
    # print('resp', resp)
    return resp


def getUserRepos(username, page, sort, direction):
    print(username, sort, direction)
    url = f'https://api.github.com/users/{username}/repos?page={page}&per_page=10&sort={sort}&direction={direction}'
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


class SortRepos:

    def __init__(self):
        self.stars = True
        self.forks = False
        self.created = False
        self.updated = False

    def sortRepos(self):
        return [
            {
                'value': self.stars,
                'name': f'{self.getPrefix(self.stars)} Most Stars',
                'sort': 'stars'
            },
            {
                'value': self.forks,
                'name': f'{self.getPrefix(self.forks)} Most Forks',
                'sort': 'forks'
            },
            {
                'value': self.created,
                'name': f'{self.getPrefix(self.created)} Recently Created',
                'sort': 'created'
            },
            {
                'value': self.updated,
                'name': f'{self.getPrefix(self.updated)} Recently Updated',
                'sort': 'updated'
            }
        ]

    def setOthers(self, sortList):
        for sort in sortList:
            if sort == 'stars':
                self.stars = False
            elif sort == 'forks':
                self.forks = False
            elif sort == 'created':
                self.created = False
            else:
                self.updated = False

    def setThisSort(self, sort):
        if sort == 'stars':
            self.stars = True
            self.setOthers(['forks', 'created', 'updated'])
        elif sort == 'forks':
            self.forks = True
            self.setOthers(['stars', 'created', 'updated'])
        elif sort == 'created':
            self.created = True
            self.setOthers(['stars', 'forks', 'updated'])
        else:
            self.updated = True
            self.setOthers(['stars', 'forks', 'created'])

    def getPrefix(self, bool):
        if bool:
            return u'\u2713'
        else:
            return '   '

    def __str__(self):
        return f'SortRep(stars = {self.stars}, forks = {self.forks}, ' \
            f'created = {self.created}, updated= {self.updated})'


class SortUsers:

    def __init__(self):
        self.best = True
        self.repos = False
        self.followers = False
        self.joined = False

    def sortUsers(self):
        return [
            {
                'value': self.best,
                'name': f'{self.getPrefix(self.best)} Best Match',
                'sort': 'best'
            },
            {
                'value': self.repos,
                'name': f'{self.getPrefix(self.repos)} Most repositories',
                'sort': 'repos'
            },
            {
                'value': self.followers,
                'name': f'{self.getPrefix(self.followers)} Most Followers',
                'sort': 'followers'
            },
            {
                'value': self.joined,
                'name': f'{self.getPrefix(self.joined)} Recently Joined',
                'sort': 'joined'
            }
        ]

    def setOthers(self, sortList):
        for sort in sortList:
            if sort == 'best':
                self.best = False
            elif sort == 'repos':
                self.repos = False
            elif sort == 'followers':
                self.followers = False
            else:
                self.joined = False

    def setThisSort(self, sort):
        if sort == 'best':
            self.best = True
            self.setOthers(['repos', 'followers', 'joined'])
        elif sort == 'repos':
            self.repos = True
            self.setOthers(['best', 'followers', 'joined'])
        elif sort == 'followers':
            self.followers = True
            self.setOthers(['best', 'repos', 'joined'])
        else:
            self.joined = True
            self.setOthers(['best', 'repos', 'followers'])

    def getPrefix(self, bool):
        if bool:
            return u'\u2713'
        else:
            return '   '

    def __str__(self):
        return f'SortRep(best = {self.best}, repos = {self.repos}, ' \
            f'followers = {self.followers}, joined= {self.joined})'


class SortUserReps:

    def __init__(self):
        self.name_asc = False
        self.name_desc = False
        self.created = False
        self.updated = True

    def sortUserReps(self):
        return [
            {
                'value': self.name_asc,
                'name': f'{self.getPrefix(self.name_asc)} Name (asc)',
                'sort': 'name_asc'
            },
            {
                'value': self.name_desc,
                'name': f'{self.getPrefix(self.name_desc)} Name (desc)',
                'sort': 'name_desc'
            },
            {
                'value': self.created,
                'name': f'{self.getPrefix(self.created)} Recently Created',
                'sort': 'created'
            },
            {
                'value': self.updated,
                'name': f'{self.getPrefix(self.updated)} Recently Updated',
                'sort': 'updated'
            }
        ]

    def setOthers(self, sortList):
        for sort in sortList:
            if sort == 'name_asc':
                self.name_asc = False
            elif sort == 'name_desc':
                self.name_desc = False
            elif sort == 'created':
                self.created = False
            else:
                self.updated = False

    def setThisSort(self, sort):
        if sort == 'name_asc':
            self.name_asc = True
            self.setOthers(['name_desc', 'created', 'updated'])
        elif sort == 'name_desc':
            self.name_desc = True
            self.setOthers(['name_asc', 'created', 'updated'])
        elif sort == 'created':
            self.created = True
            self.setOthers(['name_asc', 'name_desc', 'updated'])
        else:
            self.updated = True
            self.setOthers(['name_asc', 'name_desc', 'created'])

    def getPrefix(self, bool):
        if bool:
            return u'\u2713'
        else:
            return '   '

    def __str__(self):
        return f'SortRep(name_asc = {self.name_asc}, name_desc = {self.name_desc}, ' \
            f'created = {self.created}, updated= {self.updated})'
