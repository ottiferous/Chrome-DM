#
# Setup OAuth2Decorator Class
#

from oauth2client.appengine import OAuth2Decorator

def CreateDecorator(environment):
   'Creates the proper OAuth2Decorator for use with AppEngine'

   if environment != 'local':
      return OAuth2Decorator(
         client_id='',
         client_secret='',
         scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')
   
   else:
      return OAuth2Decorator(
         client_id='',
         client_secret='',
         scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')