from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class GitRequest(models.Model):
    REQ_TYPE = (
        ('user', 'User'),
        ('name', 'Users/name'),
        ('login', 'Users/login'),
        ('repo', 'Rep/name'),
        ('readme', 'Rep/readme'),
        ('desc', 'Rep/desc')
    )
    id = models.AutoField(primary_key=True)
    request_text = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    req_type = models.CharField(max_length=15, choices=REQ_TYPE)

    def formatDate(self):
        return self.date.strftime('%b %d, %H:%M')

    def __str__(self):
        return self.request_text + ', req_type:' + self.req_type + ', date:' + self.formatDate()


class AdvSettings(models.Model):
    id = models.AutoField(primary_key=True)
    advanced = models.BooleanField(default=False)
    followers = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    repositories = models.IntegerField(default=0)
    created = models.CharField(default='2008-04-10', max_length=10)
    updated = models.CharField(default='2008-04-10', max_length=10)

    def setConfig(self, advanced, followers, forks, stars,
                  repositories, created, updated):
        self.advanced = advanced
        self.followers = followers
        self.forks = forks
        self.stars = stars
        self.repositories = repositories
        self.created = created
        self.updated = updated
        self.save()

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

    def init_db(self):
        self.advanced = False
        self.followers = 0
        self.forks = 0
        self.stars = 0
        self.repositories = 0
        self.created = '2008-04-10'
        self.updated = '2008-04-10'
        self.save()

    def __str__(self):
        return f'{self.advanced}, {self.followers}, {self.forks}, {self.stars}, {self.repositories}, {self.created}, {self.updated}'


AdvSettings.objects.create()
# config_db = AdvSettings.objects.get(id=1)
# print(config_db)
