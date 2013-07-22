# Clean up these imports. I don't think half of them need to run.

import httplib2
import logging
import pprint
import webapp2

import os                  
import jinja2

from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.file import Storage
from oauth2client.appengine import OAuth2Decorator
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


# LocalFiles

from secretlist import OauthSecrets
from hortator import GetChromeManifest
from hortator import BuildChromeManifest
from hortator import FakeChromeManifest
from hortator import StatsFromManifest

# Determine run location
global RUNLOCATION
if os.environ['SERVER_SOFTWARE'].startswith('Development'):
   RUNLOCATION = 'local'
else:
   RUNLOCATION = 'online'

#
# OAuth Token using list unpacking from secret files
#
decorator = OAuth2Decorator( *(OauthSecrets(RUNLOCATION)) )


# Jinja Stuff Goes Here
jinja_environment = jinja2.Environment(autoescape=True,
   loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'pagetemplates')))


class Main(webapp2.RequestHandler):
   @decorator.oauth_required
   def get(self):
      response = GetChromeManifest(decorator)
      manifestTemplate = {
         'annotatedUser': u'', 'lastEnrollmentTime': u'','lastSync': u'',
         'notes': u'','orgUnitPath': u'','osVersion': u'',
         'platformVersion': u'','serialNumber': u''
      }
      stats = StatsFromManifest(response)
         
      response = BuildChromeManifest(manifestTemplate, response)
      readableList = ['User', 'First Enrollment', 'Serial Number', 'Last Sync', 'Platform Version', 'Notes', 'OS Version', 'OU Path']
         
      template = jinja_environment.get_template('index.html')
      
      self.response.out.write(template.render(
         header_list=readableList, device_page=response, 
            Channel=stats['Channel'], OUPath=stats['OUPath'], 
            Version=stats['Version'], active=stats['RecentSync'], 
            total=len(response)
         )
      )

class MakeCSV(webapp2.RequestHandler):
   @decorator.oauth_required
   def get(self):
      response = GetChromeManifest(decorator)
      manifest = {
         'annotatedLocation': u'','annotatedUser': u'','bootMode': u'','deviceId': u'',
         'firmwareVersion': u'','kind': u'','lastEnrollmentTime': u'','lastSync': u'',
         'macAddress': u'','meid': u'','model': u'','notes': u'','orderNumber': u'',
         'orgUnitPath': u'','osVersion': u'','platformVersion': u'','serialNumber': u'',
         'status': u'','supportEndDate': u'','willAutoRenew': u'' 
      }         
      response = BuildChromeManifest(manifest, response)         

      self.response.headers['Content-Type'] = 'text/csv'

      # Write the CSV Header entries
      for _ in manifest.keys():
         self.response.write( _ + "\t")
      self.response.write("\n")
      
      
      # Begin writing the device info lines
      for row in response:
         for _ in row:
            try:
               self.response.write(str(_) + "\t")
            except:
               print "ERROR parsing: ", _
         self.response.write("\n")
#      self.redirect('/')
app = webapp2.WSGIApplication( [ 
   ( '/', Main),
   ( '/csv', MakeCSV),
   (decorator.callback_path, decorator.callback_handler())
], debug=True )