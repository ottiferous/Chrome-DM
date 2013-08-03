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
  
  service = build('admin', 'directory_v1')
  request = service.chromeosdevices().list(customerId='my_customer').execute(decorator.http())
  devices = request['chromeosdevices']
  
  while 'nextPageToken' in request:
    request = service.chromeosdevices().list(customerId='my_customer', pageToken=request['nextPageToken']).execute()
    devices.append(result['chromeosdevices'])
  
  return devices
    
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
  Status = defaultdict(int)

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
  
    # Count of 'active' / 'shipped' etc.
    try:
      if 'status' in device:
        Status[device['status']] += 1
    except:
      print "[status]: ", device
        
  # Once data has been collected bundle up and return
  stats = {}
  stats['RecentSync'] = LastSyncCount
  stats['Channel'] = Channels.items()
  stats['OUPath'] = OUPath.items()
  stats['Version'] = Version.items()
  stats['Status'] = Status.items()
  
  stats['ChannelTotal'] = sum(Channels.values())
  stats['VersionTotal'] = sum(Version.values())
  
  return stats