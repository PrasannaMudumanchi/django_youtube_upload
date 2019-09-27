# django_youtube_upload

 This is a sample project fro uploading a video to youtube using Youtube Data APi V3 in Django

 I am using Django 2.1 and Python 3.7 in this project

 ## Creating Project folder and Virtual Environment
 ```
 $ mkdir django-youtube
 ```
 Clone the project
 ```
 $ git clone https://github.com/PrasannaMudumanchi/django_youtube_upload.git
 ```
 I am using Virtualenv for creating virtual environment
```
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
https://console.developers.google.com/apis/library/youtube.googleapis.com

#### Step2: Create a new Project

#### Step3: Click "Enable APIs and Services"

#### Step4: Look for "Youtube Data API V3 and Click Enable"

#### step5: You will get a message about credentials.


#### Step 6: Click on the “Create credentials” blue button on the right side, and you should get the following screen:
Choose Youtube Data API, Web Server and User data in the below screen and click on "what credentials do I need?"

#### Step7: Setup Consent Screen
Click on Setup Consent Screen on the popup as shown in below:

#### Step8: Give Required details in Oauth Consent Screen
Give details like application name and logo and support mail and click on save at the bottom of the page

#### Step9: In Step2 of Credentials, Specify Authorized Java Script origins and Authorized Redirect URIs
Specify the required details as shown in below image and Click on "Create OAuth client ID"

####  Step10: Download the Json file or you can use your Client Id or Secret key for the api in the code.

## Add GOOGLE_OAUTH2_CREDENTIALS in Settings.py file
Add GOOGLE_OAUTH2_CLIENT_ID and GOOGLE_OAUTH2_CLIENT_SECRET(only for sample purpose)
```
### google oauth credentials
GOOGLE_OAUTH2_CLIENT_ID= '<Client_id>'
GOOGLE_OAUTH2_CLIENT_SECRET = '<client_secret>'
```
**or** Add GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
```
###google oauth file
GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = '<client_Id_json file path>'
```
## Executing the project
1. Run the server and login with admin credentials
2. Authorize the user with going to `http://localhost:8000/authorize` and authorize the app
3. Upload the video through the form
4. You will get the uploaded video into your website using the Id.


