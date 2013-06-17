import gflags
import httplib2
import logging
import os
import pprint
import sys
import webapp2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.appengine import OAuth2Decorator
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


# OAuth Token
decorator = OAuth2Decorator(
   client_id='1002667537078-s6rptef9h1s7jb72ssnbvr376gs0vgds.apps.googleusercontent.com',
   client_secret='BaHkkaBxYk9d_b6cHE2iYGQ6',
   scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')

service = build('admin', 'directory_v1')


class Main(webapp2.RequestHandler):
   @decorator.oauth_required
   def get(self):  
      print 'Starting'
      if decorator.has_credentials():
         request = service.chromeosdevices().list(customerId='my_customer').execute()
         self.response.write(json.dumps(request))
      else:
         self.response.write(json.dumps({'error' : 'No credentials'}))


app = webapp2.WSGIApplication( [ 
   ( '/', Main),
   (decorator.callback_path, decorator.callback_handler())
], debug=True )