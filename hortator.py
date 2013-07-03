#
# API Call routines and modification
#


def GetChromeManifest(decorator):
   'Takes care of getting the Chrome Device Manifest. Returns the dict'
   http = decorator.http()
   try: 
      request = service.chromeosdevices().list(customerId='my_customer').execute(http=decorator.http())
      devices = request['chromeosdevices']
      
      while 'nextPageToken' in request:
         request = service.chromeosdevices().list(customerId='my_customer', pageToken=request['nextPageToken']).execute()
         devices.append(result['chromeosdevices'])
      return devices
   except:
      print 'Y\'all gonna need some credentials'

def BuildChromeManifest(manifest_template, device_list):
   'Using the template map the device list and return the result'
   try:
      built_list = []
      for _ in device_list:
         manifest_template.update(_)
         built_list.append(manifest_template.values())
      return built_list
   except:
      print device_list
      return ['#', '#', '#']

def MakeCSV(deviceList):
   'Takes the argument passed to it and creates the CSV file'
   
   manifest = {
      'annotatedLocation': u'','annotatedUser': u'','bootMode': u'','deviceId': u'',
      'firmwareVersion': u'','kind': u'','lastEnrollmentTime': u'','lastSync': u'',
      'macAddress': u'','meid': u'','model': u'','notes': u'','orderNumber': u'',
      'orgUnitPath': u'','osVersion': u'','platformVersion': u'','serialNumber': u'',
      'status': u'','supportEndDate': u'','willAutoRenew': u'' 
   }
   
   self.response.headers['Content-Type'] = 'text/csv'  
   
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
   

