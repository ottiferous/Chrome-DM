#
# Setup OAuth2Decorator Class
#


def CreateDecorator(environment):
   'Creates the proper OAuth2Decorator for use with AppEngine'

   if environment = 'local':
      return OAuth2Decorator(
         client_id='1002667537078-6b26cdfaar86uh0qfd7b8tdh5n7i14hq.apps.googleusercontent.com',
         client_secret='n0g1PahBokfDupYOhIDqPiAc',
         scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')
   
   else:
      return OAuth2Decorator(
         client_id='1002667537078-pscobeqht92tkpnjg8cghf1ssaafkrvd.apps.googleusercontent.com',
         client_secret='bgi3D7iua008KJ4SBr0F45nZ',
         scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')

