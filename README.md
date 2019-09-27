# django_youtube_upload

 This is a sample project fro uploading a video to youtube using Youtube Data APi V3 in Django

 I am using Django 2.1 and Python 3.7 in this project

 ## Creating Project folder and Virtual Environment
 I am using Virtualenv for creating virtual environment
```
   $ mkdir django-youtube
   $ cd django-youtube
   $ virtualenv --python=python3 env_djangoyt
   $ source env_djangoyt/bin/activate
```
## Installing dependencies
```
 $ pip install google-api-python-client google-auth\
 google-auth-oauthlib google-auth-httplib2 oauth2client Django unipath jsonpickle
```
## create project
```
 $ django-admin startproject django_youtube
```
## Now setup google config

#### Step1: Goto the following link and create a new project 
(https://console.developers.google.com/apis/library/youtube.googleapis.com)

