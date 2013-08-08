#
# Classes created to handle fake dictionary creation for non-Chromedevice users
#   also for unit tests
#

def FakeChromeManifest(size):
  'Creates a fake Chrome Manifest of given size'
  
  # Create dictionary of real fake places
  
  locations = [ 
    "Abu Dhabi,Abu Dhabi,United Arab Emirates",
    "Dubai,Dubai,United Arab Emirates",
    "Salta,Salta Province,Argentina",
    "Avellaneda,Buenos Aires Province,Argentina",
    "Bahia Blanca,Buenos Aires Province,Argentina",
    "Balcarce,Buenos Aires Province,Argentina",
    "Campana,Buenos Aires Province,Argentina",
    "Chacabuco,Buenos Aires Province,Argentina",
    "Del Viso,Buenos Aires Province,Argentina",
    "Isidro Casanova,Buenos Aires Province,Argentina",
    "Junin,Buenos Aires Province,Argentina",
    "La Plata,Buenos Aires Province,Argentina",
    "Lomas de Zamora,Buenos Aires Province,Argentina",
    "Luis Guillon,Buenos Aires Province,Argentina",
    "Lujan,Buenos Aires Province,Argentina",
    "Mar del Plata,Buenos Aires Province,Argentina",
    "Moron,Buenos Aires Province,Argentina",
    "Olavarria,Buenos Aires Province,Argentina",
    "Pergamino,Buenos Aires Province,Argentina",
    "Pinamar,Buenos Aires Province,Argentina",
    "Quilmes,Buenos Aires Province,Argentina"
  ]
  
  # same names
  usernames = [
    "Jacob",
    "Mason",
    "Ethan",
    "Noah",
    "William",
    "Liam",
    "Jayden",
    "Michael",
    "Alexander",
    "Aiden",
    "Daniel",
    "Matthew",
    "Elijah",
    "James",
    "Anthony",
    "Benjamin",
    "Joshua",
    "Andrew",
    "David",
    "Joseph"
  ]
  
  # Verified or dev
  bootMode = [
    "Verified",
    "Dev",
    " "
  ]
  
  # a hash following the pattern xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  deviceID = []
  
  # device name ( Alex, Stumpy, etc.)
  firmwareVersion = [
    "Alex",
    "Stumpy",
    "Lumpy",
    "Parrot",
    "Mario",
    " "
    ]
  
  # a timestamp [ 2013-07-02T16:55:45.971Z ] strip off after T for sanity sake
  lastEnrollment = []
  
  # a timestamp [ 2013-07-02T16:55:45.971Z ] strip off after T for sanity sake
  lastSync = []
  
  # device's mac address
  macAddress = []
  
  # a hexidecimal value starting AF of 16 characters total
  meid = []
  
  # not sure what could populate here - its blank on mine....
  model = []
  
  # a random note on teh device
  notes = []
  
  # a 6 digit number
  orderNumber = []

  # the device's directory folowing the pattern /xxxxxx/xxxxxx
  orgUnitPath = [
    "/",
    "/Students",
    "/Staff",
    "/Chromebooks"]
  osVersion = []
  
  # contains the channel and other info ( stripping out the other info for this)
  platformVersion = [
    "dev",
    "beta",
    "stable",
    "canary"
  ]
  
  # alpha-numeric sequence such as HY3A91ECB17898
  serialNumber = []

  # shipped and active are the most common
  status = [
    "ACTIVE",
    "SHIPPED",
    "LOST",
    "STOLEN",
    " "
  ]
  
  supportEndDate = []
  willAutoRenew = []
  
  
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