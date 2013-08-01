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
from hortator import StatsFromManifest

# Determine run location
global RUNLOCATION
if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
   RUNLOCATION = 'debug'
   debug = True
else:
   RUNLOCATION = 'online'
   debug = False

#
# OAuth Token using list unpacking from secret files
#
decorator = OAuth2Decorator( *(OauthSecrets(RUNLOCATION)) )


# Jinja Stuff Goes Here
jinja_environment = jinja2.Environment(autoescape=True,
   loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'pagetemplates')))

class BaseHandler(webapp2.RequestHandler):
  'All your Error Handling are belong to us'
  def handle_exception(self, exception, debug):
    # Log the error
    logging.exception(exception)
    print "==================================="
    print exception._get_reason()
    print type(exception)
    print "==================================="

    if isinstance(exception, webapp2.HTTPException):
      self.response.set_status(exception.code)
    else:
      self.response.set_status(500)

    template = jinja_environment.get_template('error.html')
    self.response.out.write(template.render(messageobj=exception._get_reason()))

class Main(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render())
  

class SetupPage(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('setup.html')
    self.response.out.write(template.render())
  

class AboutPage(BaseHandler):
  def get(self):
      template = jinja_environment.get_template('about.html')
      self.response.out.write(template.render())
  

class StatsPage(BaseHandler):
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
       
      template = jinja_environment.get_template('statspage.html')
    
      self.response.out.write(template.render(
         header_list=readableList, device_page=response, 
            Channel=stats['Channel'], OUPath=stats['OUPath'], 
            Version=stats['Version'], active=stats['RecentSync'], 
            total=len(response)
         )
      )
      
class MakeCSV(BaseHandler):
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

      # Specify headers for a CSV download
      self.response.headers['Content-Type'] = 'application/csv'
      self.response.headers.add_header('content-disposition', 'attachment', filename='devicelist.csv')

      # Write the CSV Header entries
      for _ in manifest.keys():
         self.response.write( "\"" + _ + "\"" + ",")
      self.response.write("\n")
      
      
      # Begin writing the device info lines
      for row in response:
         for _ in row:
            try:
               self.response.write("\"" + str(_) + "\"" + ",")
            except:
               print "[ERROR parsing]: ", _
         self.response.write("\n")

def handle_403(request, response, exception):
   logging.exception(exception)
   response.write('Ooops! You\'re gonna need authorization to do that')
   response.set_status(403)         
    
app = webapp2.WSGIApplication( [ 
   ( '/', Main),
   ( '/csv', MakeCSV),
   ( '/stats', StatsPage),
   ( '/about', AboutPage),
   ( '/setup', SetupPage),
   (decorator.callback_path, decorator.callback_handler())
], debug=debug )

app.error_handlers[403] = handle_403