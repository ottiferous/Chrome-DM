#
# Python Manifest for Chrome devices
#

class chromeManifest:
   'Contains all information for Chrome'
   def __init__():
      manifest = {
         'annotatedLocation': '',
         'annotatedUser': '',
         'bootMode': '',
         'deviceId': '',
         'firmwareVersion': '',
         'kind': '',
         'lastEnrollmentTime': '',
         'lastSync': '',
         'macAddress': '',
         'meid': '',
         'model': '',
         'notes': '',
         'orderNumber': '',
         'orgUnitPath': '',
         'osVersion': '',
         'platformVersion': '',
         'serialNumber': '',
         'status': '',
         'supportEndDate': '',
         'willAutoRenew': '' 
      }
#
# Gets the RAW response and begins cleaning it up. This is very static and should be cleaned up
# Returns an array of dict objects
#
   def serialize(apiCall):
      del apiCall['kind']
      finalVersion = []
      for _ in apiCall['chromeosdevices']:
         finalVersion.append(_)
   return finalVersion
   
#
# Passes a ChromeOS device dictionary over so it can match up with the master manifest above
# does not change the manifest file, this is a placeholder. The returned file is used instead
#
   def entryUpdate(chromeDevice):
      list = []
      for _ in chromeDevice:
         manifest.update(_)
         list.append(manifest)
      return list

#
# Create the string object of all the devices - each line should be an entry in a list
#
   def makeCSV(deviceList):
      list = []
      for _ in deviceList:
         line = []
         for key, value in _.iteritems()
            line.append(v)
         list.append(line)
      for _ in list:
         print ','.join(_)
      return list