from django.shortcuts import render
from django import forms
from django.views.generic import FormView

### imports for authorize view
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic.base import View

from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from .models import CredentialsModel

## imports for callbackview and home page view
import tempfile
from django.http import HttpResponse, HttpResponseBadRequest
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

flow = OAuth2WebServerFlow(
            client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/youtube',
            redirect_uri='http://localhost:8000/oauth2callback/')
# flow = flow_from_clientsecrets(
#             settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
#             scope='https://www.googleapis.com/auth/youtube',
#             redirect_uri='http://localhost:8000/oauth2callback/')

class YouTubeForm(forms.Form):
    video = forms.FileField()

class HomePageView(FormView):
    template_name = 'core/home.html'
    form_class = YouTubeForm

    def form_valid(self, form):
        fname = form.cleaned_data['video'].temporary_file_path()

        storage = DjangoORMStorage(
            CredentialsModel, 'id', self.request.user.id, 'credential')
        credentials = storage.get()

        client = build('youtube', 'v3', credentials=credentials)

        body = {
            'snippet': {
                'title': 'Sample Video Two',
                'description': 'Sample Video Two Description',
                'tags': 'django,howto,video,api',
                'categoryId': '22'
            },
            'status': {
                'privacyStatus': 'unlisted'
            }
        }

        with tempfile.NamedTemporaryFile('wb', suffix='yt-django') as tmpfile:
            with open(fname, 'rb') as fileobj:
                tmpfile.write(fileobj.read())
                insert_request = client.videos().insert(
                    part=','.join(body.keys()),
                    body=body,
                    media_body=MediaFileUpload(
                        tmpfile.name, chunksize=-1, resumable=True)
                )
                response = insert_request.execute()
                video_id = response['id']
                # html = '<html><body><a href="https://www.youtube.com/watch?v={0}">Uploaded Video link</a></body></html>'.format(video_id)
                html = '<html><body><iframe width="420" height="315" src="https://www.youtube.com/embed/{0}"></iframe></body></html>'.format(video_id)

        return HttpResponse(html)

    

class AuthorizeView(View):

    def get(self, request, *args, **kwargs):
        storage = DjangoORMStorage(
            CredentialsModel, 'id', request.user.id, 'credential')
        credential = storage.get()

        if credential is None or credential.invalid == True:
            flow.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY, request.user)
            authorize_url = flow.step1_get_authorize_url()
            return redirect(authorize_url)
        return redirect('/')
        

        # or if you downloaded the client_secrets file

class Oauth2CallbackView(View):

    def get(self, request, *args, **kwargs):
        if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.GET.get('state').encode(),
            request.user):
                return HttpResponseBadRequest()
        credential = flow.step2_exchange(request.GET)
        storage = DjangoORMStorage(
            CredentialsModel, 'id', request.user.id, 'credential')
        storage.put(credential)
        return redirect('/')    
        