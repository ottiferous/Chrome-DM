#
# API Call routines and modification
#

from apiclient.discovery import build
from apiclient.errors import HttpError

# Needed for Stats
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
import re

#
#  The query is up and running
#
def GetChromeManifest(decorator):
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

def FakeChromeManifest():
  'Returns a faked response to save on API calls'
  
  return [{u'status': u'ACTIVE', u'lastSync': u'2013-04-24T00:40:10.404Z', u'annotatedLocation': u'Mountain View <-> Burlingame', u'annotatedUser': u'Andrew', u'deviceId': u'60616baa-4140-436b-b3f4-ae8d64702e6d', u'platformVersion': u'1660.144.0 (Official Build) stable-channel x86-alex', u'osVersion': u'18.0.1025.168', u'firmwareVersion': u'Alex.03.61.0735.0056G3.0021', u'lastEnrollmentTime': u'2013-01-09T17:05:57.838Z', u'kind': u'admin#directory#chromeosdevice', u'notes': u'Req-Tag:368411', u'serialNumber': u'HG3D93CB601768', u'bootMode': u'Verified', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2012-08-21T16:44:26.875Z', u'kind': u'admin#directory#chromeosdevice', u'lastEnrollmentTime': u'2012-06-15T20:55:51.421Z', u'serialNumber': u'HT4L91SC300149', u'deviceId': u'9cd7ddbc-b09e-4438-a1a7-58052b8319c4', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-03-15T21:26:51.700Z', u'kind': u'admin#directory#chromeosdevice', u'annotatedUser': u'andrew@skip-shot.net', u'deviceId': u'b1dc1b53-362d-4f8d-98a6-5832346c5b21', u'lastEnrollmentTime': u'2013-03-15T21:26:50.597Z', u'orgUnitPath': u'/', u'notes': u'', u'serialNumber': u'HJAC93CB702652', u'annotatedLocation': u''}, {u'status': u'ACTIVE', u'lastSync': u'2013-01-30T17:13:49.873Z', u'kind': u'admin#directory#chromeosdevice', u'lastEnrollmentTime': u'2013-01-30T01:17:31.886Z', u'serialNumber': u'HG3D93CB600328', u'deviceId': u'c558d540-93a7-46f1-8a9e-b2049cdf5e86', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-01-16T23:52:13.487Z', u'kind': u'admin#directory#chromeosdevice', u'lastEnrollmentTime': u'2013-01-16T23:46:04.757Z', u'serialNumber': u'HY3A91ECB17898', u'deviceId': u'ca34540c-ede5-4529-88b5-9b3214737db6', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-06-17T17:36:51.571Z', u'deviceId': u'cad63fdb-4d6f-46e1-8c3e-43939544c6f8', u'platformVersion': u'4191.0.0 (Official Build) dev-channel daisy', u'osVersion': u'29.0.1520.2', u'firmwareVersion': u'Google_Snow.2695.117.0', u'lastEnrollmentTime': u'2013-06-11T17:35:24.820Z', u'kind': u'admin#directory#chromeosdevice', u'serialNumber': u'HY3B91ECA00144', u'bootMode': u'Verified', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-05-15T21:54:16.206Z', u'deviceId': u'e4d11d6a-1de8-46e7-8e29-8644f13ffe34', u'platformVersion': u'3701.81.2 (Official Build) stable-channel lumpy', u'osVersion': u'26.0.1410.57', u'firmwareVersion': u'Google_Lumpy.2.111.0', u'lastEnrollmentTime': u'2013-05-02T16:54:31.783Z', u'kind': u'admin#directory#chromeosdevice', u'serialNumber': u'HTKH91SC500127', u'bootMode': u'Verified', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-05-09T00:02:32.205Z', u'annotatedLocation': u'', u'annotatedUser': u'', u'deviceId': u'14743d14-50cf-4582-b7fa-48d2770167f2', u'platformVersion': u'2913.276.0 (Official Build) stable-channel x86-alex', u'osVersion': u'23.0.1271.110', u'firmwareVersion': u'Alex.03.61.0735.0056G3.0021', u'lastEnrollmentTime': u'2012-09-13T23:32:56.071Z', u'kind': u'admin#directory#chromeosdevice', u'notes': u'Moo-cow unit.', u'serialNumber': u'GZTB93CB600177', u'bootMode': u'Verified', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-04-29T22:54:11.145Z', u'kind': u'admin#directory#chromeosdevice', u'lastEnrollmentTime': u'2013-04-29T22:54:10.322Z', u'serialNumber': u'Andrew', u'deviceId': u'77bc2a28-7e01-4fd9-9f1a-aeeff74e82c5', u'orgUnitPath': u'/Students/Subdomain'}, {u'status': u'ACTIVE', u'lastSync': u'2013-05-21T16:28:47.318Z', u'kind': u'admin#directory#chromeosdevice', u'annotatedUser': u'andrew@skip-shot.net', u'deviceId': u'8e56e870-a02c-4cf6-ba5e-4b01a9242015', u'lastEnrollmentTime': u'2013-05-21T16:26:27.803Z', u'serialNumber': u'HTKF91YC400591', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-03-01T23:23:39.752Z', u'kind': u'admin#directory#chromeosdevice', u'lastEnrollmentTime': u'2012-11-21T19:16:02.789Z', u'serialNumber': u'HY3B91ECA01120', u'deviceId': u'94e3f089-75e1-48c0-ba86-e948528c427a', u'orgUnitPath': u'/'}, {u'status': u'ACTIVE', u'lastSync': u'2013-04-30T18:21:01.123Z', u'kind': u'admin#directory#chromeosdevice', u'lastEnrollmentTime': u'2013-04-30T16:46:18.045Z', u'serialNumber': u'HG3D93CB701951', u'deviceId': u'd3b704ae-27d5-4a51-9052-1defb4f5a38b', u'orgUnitPath': u'/testoferous'}]
  
def BuildChromeManifest(Template, apiResponse):
  'Use the supplied template for mapping desired information and returning new manifest'

  holder = []
  for device_info in apiResponse:
    for key in Template:
      Template[key] = device_info.get(key, " ")
    holder.append(Template.values())
  return holder

def StatsFromManifest(apiResponse):
  'Perform a series of tests on Chrome Manifest and returns a dict object'

  today = datetime.now().date()
  LastSyncCount = 0
  Channels = defaultdict(int)
  OUPath = defaultdict(int)
  Version = defaultdict(int)

  # Master loop - go through all devices
  for device in apiResponse:

    # Check for LastSyncTime
    try:
      if 'lastSync' in device:
        if (today - (datetime.strptime(device['lastSync'][:-14], '%Y-%m-%d').date())) >= timedelta(days=-7):
          LastSyncCount += 1
    except:
      print "[LastSync]: ", device
      
    # Find the channel and increment appropriately    
    try:
      if 'platformVersion' in device:
        Channels[re.match(r'.* (.*)-channel', device['platformVersion'], re.U).group(1)] += 1 
    except:
      print "[platformVersion]: ", device

    # Count of each device in a given OU
    try:
      if 'orgUnitPath' in device:
        OUPath[device['orgUnitPath']] += 1
    except:
      print "[orgUnitPath]", device

    # Count of each OS Version
    try:
      if 'osVersion' in device:
        Version[device['osVersion']] += 1
    except:
      print "[osVersion]: ", device

  # Once data has been collected bundle up and return
  stats = {}
  stats['RecentSync'] = LastSyncCount
  stats['Channel'] = Channels.items()
  stats['OUPath'] = OUPath.items()
  stats['Version'] = Version.items()
  
  return stats