import gflags
import httplib2
import logging
import os
import pprint
import sys
import webapp2

from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.file import Storage
from oauth2client.appengine import OAuth2Decorator
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


# OAuth Token
decorator = OAuth2Decorator(
   client_id='1002667537078-pscobeqht92tkpnjg8cghf1ssaafkrvd.apps.googleusercontent.com',
   client_secret='bgi3D7iua008KJ4SBr0F45nZ',
   scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')

service = build('admin', 'directory_v1')


class Main(webapp2.RequestHandler):
   @decorator.oauth_required
   def get(self):  
      http = decorator.http()
      if decorator.has_credentials():
         request = service.chromeosdevices().list(customerId='my_customer').execute(decorator.http())
         self.response.write(request)
      else:
         self.response.write('Y\'all gonna need some credentials')


app = webapp2.WSGIApplication( [ 
   ( '/', Main),
   (decorator.callback_path, decorator.callback_handler())
], debug=True )