# Generated by Django 2.1 on 2019-09-27 05:43

from django.db import migrations, models
import oauth2client.contrib.django_util.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credential', oauth2client.contrib.django_util.models.CredentialsField(null=True)),
            ],
        ),
    ]
