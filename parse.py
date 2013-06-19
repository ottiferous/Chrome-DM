#
# Takes the API return value and parse it into different formats.
#
#        j['chromeosdevices'][1].values()


# Unpack and prepare for CSV
# determine which key/value pair has the longest length to make the CSV header with all info
# assing this value to the header[] tuple, and then give it values based on those found in the
# response object

def Manifest_to_CSV(response):
   header = []
   response