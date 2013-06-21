import gflags
import httplib2
import logging
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
      self.response.headers['Content-Type'] = 'text/csv'  
      http = decorator.http()
      if decorator.has_credentials():
         request = service.chromeosdevices().list(customerId='my_customer').execute(decorator.http())
         devices = request['chromeosdevices']

         while 'nextPageToken' in request:
            request = service.chromeosdevices().list(customerId='my_customer', pageToken=request['nextPageToken']).execute()
            devices.append(result['chromeosdevices'])
         print "Devices is: ", len(devices)
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
         
         print "deviceList is: ", len(deviceList)   
         # Write the Header info
         for _ in manifest.keys():
            self.response.write( _ + '\t')
         self.response.write("\n")
         
         
         # Begin writing the device info lines
         for _ in deviceList:
            map(str, _)
            try:
               self.response.write("\t".join(map(lambda x:x if x!= '' else ' ',_)))
               self.response.write("\n")
            except:
               print "Error with: ", _
      else:
         self.response.write('Y\'all gonna need some credentials')


app = webapp2.WSGIApplication( [ 
   ( '/', Main),
   (decorator.callback_path, decorator.callback_handler())
], debug=True )