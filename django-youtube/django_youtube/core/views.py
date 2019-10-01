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
from .models import CredentialsModel, VideoDetails

## imports for callbackview and home page view
import tempfile
from django.http import HttpResponse, HttpResponseBadRequest
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

### This is for fetching data using requests
import requests

### authflow using client id and client secret
flow = OAuth2WebServerFlow(
            client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/youtube',
            redirect_uri='http://localhost:8000/oauth2callback/')
### authflow using client Secret
# flow = flow_from_clientsecrets(
#             settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
#             scope='https://www.googleapis.com/auth/youtube',
#             redirect_uri='http://localhost:8000/oauth2callback/')

### form for uploading a video
class YouTubeForm(forms.Form):
    video = forms.FileField()

### code for uploading video to youtube
# Here the credentials field get the credentials stored in the CredentialsModel and create a build service
# then get the file in temporary file and upload it using client.videos().insert function


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
                'privacyStatus': 'public'
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
                print(response)
                video_id = response['id']
                channel_id = response['snippet']['channelId'] 
                print(channel_id)
                video_url = 'https://www.googleapis.com/youtube/v3/videos'
                video_params = {
                    'part': 'statistics',
                    'key': settings.GOOGLE_API_KEY,
                    'id': video_id
                }
                r = requests.get(video_url, params=video_params)
                results = r.json()['items']
                print(results)
                context = {
                    'video_id':video_id,
                    'stats':results
                }
                video_details = VideoDetails(
                    video_id = video_id,
                    channel_id = channel_id
                )
                video_details.save()
                # html = '<html><body><a href="https://www.youtube.com/watch?v={0}">Uploaded Video link</a></body></html>'.format(video_id)
                # html = '<html><body><iframe width="1200" height="600" src="https://www.youtube.com/embed/{0}"></iframe></body></html>'.format(video_id)

        # return HttpResponse(html)
        return render(self.request,'core/uploaded_videos.html',context)

#### get video statistics using video_id
# This has been done with the reference of this video link https://www.youtube.com/watch?v=lc2KvFbbfAQ
# This has been done using requests package
def search_video(request):
   search_url = 'https://www.googleapis.com/youtube/v3/search'
   video_url = 'https://www.googleapis.com/youtube/v3/videos'
   video_params = {
       'part': 'status,statistics,localizations',
       'key': settings.GOOGLE_API_KEY,
       'id': '<video_id>'
   }
   r = requests.get(video_url, params=video_params)
   results = r.json()
   print(results)
   return render(request, 'core/video_details.html',{'results':results})

#### get channel videos

# This code is written based on the reference taken from this video link: https://www.youtube.com/watch?v=IK5UUrPglTM
# In this we get the playlist id i.e UploadsPlaylistId of specific channel at first 
# then we get the videos i.e playlistItems
# then we get the statistics of every video in video_stats

def get_channel_videos(request):
   
   # get Uploads playlist id
   youtube = build('youtube', 'v3', developerKey=settings.GOOGLE_API_KEY)
   res = youtube.channels().list(id='<channel_id>',
                                 part='contentDetails').execute()
   playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
   
   videos = []
   video_stats = []
   next_page_token = None
   
   while 1:
       res = youtube.playlistItems().list(playlistId=playlist_id,
                                          part='snippet',
                                          maxResults=50,
                                          pageToken=next_page_token).execute()
       videos += res['items']
       next_page_token = res.get('nextPageToken')
       
       if next_page_token is None:
           break
   for video in videos:
       print(video['snippet']['title'])
       video_id = video['snippet']['resourceId']['videoId']
       video_url = 'https://www.googleapis.com/youtube/v3/videos'
       video_params = {
            'part': 'statistics',
            'key': settings.GOOGLE_API_KEY,
            'id': video_id
        }
       r = requests.get(video_url, params=video_params)
       results = r.json()
       video_stats.append(results)
       print(results)


   context = {
       'videos': videos,
       'video_stats':video_stats,
       # 'url': f'https://www.youtube.com/watch?v=',
   }

   return render(request, 'core/channel_details.html', context)
    

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
        