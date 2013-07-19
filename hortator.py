#
# API Call routines and modification
#

from apiclient.discovery import build
from apiclient.errors import HttpError

#
#  The query is up and running
#
def GetChromeManifest(location, decorator):
   'Takes care of getting the Chrome Device Manifest. Returns the dict'
   
   try: 
      service = build('admin', 'directory_v1')
      request = service.chromeosdevices().list(customerId='my_customer').execute(decorator.http())
      devices = request['chromeosdevices']
      
      while 'nextPageToken' in request:
         request = service.chromeosdevices().list(customerId='my_customer', pageToken=request['nextPageToken']).execute()
         devices.append(result['chromeosdevices'])
      
      return devices
   except HttpError as err:
      print '[ERROR]: ', err.content

def BuildChromeManifest(Template, apiResponse):
   'Use the supplied template for mapping desired information and returning new manifest'

   holder = []
   for device_info in apiResponse:
      for key in Template:
         Template[key] = device_info.get(key, " ")
      holder.append(Template.values())
   return holder


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
   

