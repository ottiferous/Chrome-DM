#
# API Call routines and modification
#

from secretlist import OauthSecrets 
from oauth2client.appengine import OAuth2Decorator
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets
from apiclient.discovery import build


def GetChromeManifest(location):
   'Takes care of getting the Chrome Device Manifest. Returns the dict'

   decorator = OAuth2Decorator( *(OauthSecrets(location)) )
   service = build('admin', 'directory_v1')

   try: 
      request = service.chromeosdevices().list(customerId='my_customer').execute(http=decorator.http())
      devices = request['chromeosdevices']
      
      while 'nextPageToken' in request:
         request = service.chromeosdevices().list(customerId='my_customer', pageToken=request['nextPageToken']).execute()
         devices.append(result['chromeosdevices'])
      
      return devices
   except:
      print '[ERROR]: Unable to retrieve CrOS manifest'

def BuildChromeManifest(desiredTemplate, apiResponse):
   'Use the supplied template for mapping desired information and returning new manifest'
   try:
      builtDictionary = []
      for _ in apiResponse:
         desiredTemplate.update(_)
         builtDictionary.append(desiredTemplate.values())
      return builtDictionary
   except:
      print apiResponse
      return ['#', '#', '#']

def MakeCSV(apiResponse):
   'Takes the raw API Response and outputs all info to a CSV'
   
   manifest = {
      'annotatedLocation': u'','annotatedUser': u'','bootMode': u'','deviceId': u'',
      'firmwareVersion': u'','kind': u'','lastEnrollmentTime': u'','lastSync': u'',
      'macAddress': u'','meid': u'','model': u'','notes': u'','orderNumber': u'',
      'orgUnitPath': u'','osVersion': u'','platformVersion': u'','serialNumber': u'',
      'status': u'','supportEndDate': u'','willAutoRenew': u'' 
   }
   
   self.response.headers['Content-Type'] = 'text/csv'  
   
   csvList = []
   for _ in devices:
      manifest.update(_)
      csvList.append(manifest.values())
      
   # Write the Header info
   for _ in manifest.keys():
      self.response.write( _ + "\t")
   self.response.write("\n")
   
   # Begin writing the device info lines
   for row in csvList:
      for _ in row:
         try:
            self.response.write(str(_) + "\t")   
         except:
            print "ERROR parsing: ", _
      self.response.write("\n")
   

