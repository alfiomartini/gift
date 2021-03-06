from datetime import datetime

# https://stackoverflow.com/questions/1383239/can-i-use-init-py-to-define-global-variables


class Config:

    def __init__(self):
        self.advanced = False
        self.followers = 0
        self.forks = 0
        self.stars = 0
        self.repositories = 0
        # Github came out in April 10, 2008
        # self.created = datetime(2008, 4, 10)
        self.created = '2008-04-10'
        # self.updated = datetime(2008, 4, 10)
        self.updated = '2008-04-10'

    def setConfig(self, advanced, followers, forks, stars,
                  repositories, created, updated):
        self.advanced = advanced
        self.followers = followers
        self.forks = forks
        self.stars = stars
        self.repositories = repositories
        self.created = created
        self.updated = updated

    def setOneConfig(self, param, val):
        if param == 'advanced':
            self.advanced = val
        elif param == 'followers':
            self.followers = val
        elif param == 'forks':
            self.forks = val
        elif param == 'stars':
            self.stars = val
        elif param == 'repositories':
            self.repositories = val
        elif param == 'created':
            self.created = val
        else:
            self.updated = val

    def getConfig(self, param):
        if param == 'advanced':
            return self.advanced
        elif param == 'followers':
            return self.followers
        elif param == 'forks':
            return self.forks
        elif param == 'stars':
            return self.stars
        elif param == 'repositories':
            return self.repositories
        elif param == 'created':
            return self.created
        else:
            return self.updated

    def getConfigAll(self):
        return {
            'advanced': self.advanced,
            'followers': self.followers,
            'forks': self.forks,
            'stars': self.stars,
            'repositories': self.repositories,
            'created': self.created,
            'updated': self.updated,
        }

    def __str__(self):
        d_created = self.created.strftime('%b %d, %Y')
        d_updated = self.updated.strftime('%b %d, %Y')
        return f'advanced = {self.advanced}, created = {d_created}, updated = {d_updated}'


config = Config()
