from datetime import datetime

# https://stackoverflow.com/questions/1383239/can-i-use-init-py-to-define-global-variables


class Config:

    def __init__(self):
        self.advanced = False
        self.followers = 0
        self.forks = 0
        self.stars = 0
        # Github came out in April 10, 2008
        self.start_date = datetime(2008, 4, 9)
        self.end_date = datetime(2008, 4, 9)

    def setConfig(advanced, folllowers, forks, stars, start_date, end_date):
        self.advanced = advanced
        self.followers = folllowers
        self.forks = forks
        self.stars = stars
        self.start_date = start_date
        self.end_date = end_date

    def setOneConfig(self, param, val):
        if param == 'advanced':
            self.advanced = val
        elif param == 'followers':
            self.followers = val
        elif param == 'forks':
            self.forks = val
        elif param == 'stars':
            self.stars = val
        elif param == 'start_date':
            self.start_date = val
        else:
            self.end_date = val

    def getConfig(self, param):
        if param == 'advanced':
            return self.advanced
        elif param == 'followers':
            return self.followers
        elif param == 'forks':
            return self.forks
        elif param == 'stars':
            return self.stars
        elif param == 'start_date':
            return self.start_date
        else:
            return self.end_date

    def __str__(self):
        start_date = self.start_date.strftime('%b %d, %Y')
        end_date = self.end_date.strftime('%b %d, %Y')
        return f'advanced = {self.advanced}, start_date = {start_date}, end_date = {end_date}'


config = Config()
