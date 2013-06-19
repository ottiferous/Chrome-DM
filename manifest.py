#
# Python Master 
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
#
   def addEntry(list):
      for each _ in list:
         manifest[_].append(list[_])