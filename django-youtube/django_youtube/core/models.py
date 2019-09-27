from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField
from django.contrib.auth.models import User


class CredentialsModel(models.Model):
    credential = CredentialsField()