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
    
    # Calculate percentages
    total = len(response)
    VProunded = 100*round(float(stats['VersionTotal']) / float(total),2)
    CProunded = 100*round(float(stats['ChannelTotal']) / float(total),2)
    AProunded = 100*round(float(stats['RecentSync']) / float(total),2)
   
    self.response.out.write(template.render(
      header_list=readableList, device_page=response, 
        Channel=stats['Channel'], OUPath=stats['OUPath'], 
        Version=stats['Version'], active=stats['RecentSync'],
        VersionTotal=stats['VersionTotal'], VersionPercent=VProunded,
        ChannelTotal=stats['ChannelTotal'], ChannelPercent=CProunded,
        Status=stats['Status'],
        ActivePercentage=AProunded ,total=total
      )
    )
    
class MakeCSV(BaseHandler):
  @decorator.oauth_required
  def get(self):
    response = GetChromeManifest(decorator)
    manifest = {
      'annotatedLocation': u'','annotatedUser': u'','bootMode': u'','deviceId': u'',
      'firmwareVersion': u'','lastEnrollmentTime': u'','lastSync': u'',
      'macAddress': u'','meid': u'','model': u'','notes': u'','orderNumber': u'',
      'orgUnitPath': u'','osVersion': u'','platformVersion': u'','serialNumber': u'',
      'status': u'','supportEndDate': u'','willAutoRenew': u'' 
    }      
    response = BuildChromeManifest(manifest, response)      

    # Specify headers for a CSV download
    self.response.headers['Content-Type'] = 'application/csv'
    self.response.headers.add_header('content-disposition', 'attachment', filename='devicelist.csv')

    # Write the CSV Header entries
    line = ""
    for _ in manifest.keys():
      line += ( "\"" + _ + "\"" + ",")
    self.response.write(line[:-1] + "\n")
    
    
    # Begin writing the device info lines
    for row in response:
      line = ""
      for _ in row:
        line += ("\"" + str(_) + "\"" + ",")
      self.response.write(line[:-1] + "\n")

   
app = webapp2.WSGIApplication( [ 
  ( '/', Main),
  ( '/csv', MakeCSV),
  ( '/stats', StatsPage),
  ( '/about', AboutPage),
  ( '/setup', SetupPage),
  (decorator.callback_path, decorator.callback_handler())
], debug=debug )