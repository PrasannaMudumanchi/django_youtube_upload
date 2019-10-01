from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField
from django.db.models import CharField
from django.contrib.auth.models import User


class CredentialsModel(models.Model):
    credential = CredentialsField()

class VideoDetails(models.Model):
    video_id = CharField(max_length=30)
    channel_id = CharField(max_length=30)