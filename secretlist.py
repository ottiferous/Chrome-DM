#
# Setup OAuth2Decorator Class
#

from oauth2client.appengine import Oauth2Decorator
from oauth2client.appengine import OAuth2Decorator

def CreateDecorator(environment):
   'Creates the proper OAuth2Decorator for use with AppEngine'

   if environment = 'local':    #for running locally through AppEngine SDK
      return OAuth2Decorator(
         client_id='YOUR_CLIENT_ID_HERE',
         client_secret='YOU_CLIENT_SECRET_HERE',
         scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')
   
   else:
      return OAuth2Decorator(
         client_id='YOUR_CLIENT_ID_HERE,
         client_secret='YOU_CLIENT_SECRET_HERE',
         scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')