import os, re
from datetime import datetime
from urlparse import urlparse
import gdata.auth
import gdata.calendar.service
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):
  def get(self):
    template_values = {}

    user = users.get_current_user()
    if user and self.check_email(user):
      greeting = ('Hello %s (%s)!)' %
                 (user.email(), user.nickname()))
      event = self.get_next_event(user)
      if event:
        template_values['title'] = event.title.text
        template_values['start'] = event.when[0].start_time
        template_values['end'] = event.when[0].end_time
        template_values['where'] = event.where[0].value_string
        template_values['desc'] = event.content.text
    else:
      greeting = 'You need to log in!'

    template_values['greeting'] = greeting
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, template_values))

  def check_email(self, user):
    """Performs basic validation of the supplied email address as outlined
    in http://code.google.com/googleapps/marketplace/best_practices.html
    """
    domain = urlparse(user.federated_identity()).hostname
    m = re.search('.*@' + domain, user.email())
    if m:
      return True
    else:
      return False

  def get_next_event(self, user):
    """Uses two-legged OAuth to retrieve the user's next Calendar event."""
    CONSUMER_KEY = "replace_me.apps.googleusercontent.com"
    CONSUMER_SECRET = "replace_me"
    SIG_METHOD = gdata.auth.OAuthSignatureMethod.HMAC_SHA1

    client = gdata.calendar.service.CalendarService(source='myCompany-helloworld')
    client.SetOAuthInputParameters(SIG_METHOD, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                                   two_legged_oauth=True, requestor_id=user.email())

    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full')
    query.start_min = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    query.sortorder = 'ascending'
    query.orderby = 'starttime'
    query.max_results = 1
    feed = client.CalendarQuery(query)

    if len(feed.entry):
      return feed.entry[0]
    else:
      return None

class OpenIDHandler(webapp.RequestHandler):
    def get(self):
      """Begins the OpenID flow and begins Google Apps discovery for the supplied domain."""
      self.redirect(users.create_login_url(dest_url='http://my-app.appspot.com/',
                                           _auth_domain=None,
                                           federated_identity=self.request.get('domain')))

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/_ah/login_required', OpenIDHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()