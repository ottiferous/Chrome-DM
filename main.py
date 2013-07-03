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

# OAuth Token using list unpacking from secret files
decorator = OAuth2Decorator( *(OauthSecrets('local')) )

# comment out the line below to work offline
service = build('admin', 'directory_v1')

# Jinja Stuff Goes Here
jinja_environment = jinja2.Environment(autoescape=True,
   loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'pagetemplates')))


class Main(webapp2.RequestHandler):
   @decorator.oauth_required
   def get(self):
      self.response.headers['Content-Type'] = 'text/csv'  
      http = decorator.http()
      if decorator.has_credentials():
         request = service.chromeosdevices().list(customerId='my_customer').execute(decorator.http())
         devices = request['chromeosdevices']
         while 'nextPageToken' in request:
            request = service.chromeosdevices().list(customerId='my_customer', pageToken=request['nextPageToken']).execute()
            devices.append(result['chromeosdevices'])
         manifest = {
            'annotatedLocation': u'','annotatedUser': u'','bootMode': u'','deviceId': u'',
            'firmwareVersion': u'','kind': u'','lastEnrollmentTime': u'','lastSync': u'',
            'macAddress': u'','meid': u'','model': u'','notes': u'','orderNumber': u'',
            'orgUnitPath': u'','osVersion': u'','platformVersion': u'','serialNumber': u'',
            'status': u'','supportEndDate': u'','willAutoRenew': u'' 
         }         
         # create a manfiest with blanks for empty fields
         deviceList = []
         for _ in devices:
            manifest.update(_)
            deviceList.append(manifest.values())
         
         # Write the Header info
         for _ in manifest.keys():
            self.response.write( _ + "\t")
         self.response.write("\n")
         
         
         # Begin writing the device info lines
         for row in deviceList:
            for _ in row:
               try:
                  self.response.write(str(_) + "\t")
               except:
                  print "ERROR parsing: ", _
            self.response.write("\n")
            
      else:
         self.response.write('Y\'all gonna need some credentials')

class MakeCSV(webapp2.RequestHandler):
   def get(self):
      self.response.write("Coming soon...")

class RenderMain(webapp2.RequestHandler):
   @decorator.oauth_required
   def get(self):
      manifest_template = {
         'annotatedUser': u'', 'kind': u'','lastEnrollmentTime': u'','lastSync': u'',
         'model': u'','notes': u'','orgUnitPath': u'','osVersion': u'',
         'platformVersion': u'','serialNumber': u'' }
      built_list = []
      devices = False

      http = decorator.http()
      if decorator.has_credentials():
         print "[DECORATOR]: ", decorator
         request = service.chromeosdevices().list(customerId='my_customer').execute(decorator.http())
         devices = request['chromeosdevices']
      
         while 'nextPageToken' in request:
            request = service.chromeosdevices().list(customerId='my_customer', pageToken=request['nextPageToken']).execute()
            devices.append(result['chromeosdevices'])
         
         for _ in devices:
            manifest_template.update(_)
            built_list.append(manifest_template.values())
      else:
         print "Something went wrong!"
         print " = Dumping variables = "
         print "[HTTP]: ", http
         print "[DEVICES]: ", devices
         print "[BUILT_LIST]: ", built_list
         print "[DECORATOR]: ", decorator.iteritems()
      
      
      readable_list = ['User', 'Kind', 'Enrollment Time', 'Last Sync', 
                'Model', 'Notes', 'OU Path', 'OS Version', 
                'Platform Version', 'Serial Number']
               
      template = jinja_environment.get_template('index.html')
      self.response.out.write(template.render(header_list=readable_list, device_page=built_list))

app = webapp2.WSGIApplication( [ 
   ( '/', Main),
   ( '/csv', MakeCSV),
   ( '/render', RenderMain),
   (decorator.callback_path, decorator.callback_handler())
], debug=True )