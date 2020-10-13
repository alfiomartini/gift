from django.db import models
from django.utils import timezone

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

    def __str__(self):
        return self.request_text + ', req_type:' + self.req_type
