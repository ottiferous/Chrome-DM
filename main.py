# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gflags
import httplib2
import logging
import os
import pprint
import sys
import webapp2

from apiclient.discovery import build
#from google.appengine.ext import webapp
from oauth2client.file import Storage
from oauth2client.appengine import OAuth2Decorator
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


# OAuth Token
decorator = OAuth2Decorator(
	client_id='1002667537078-s6rptef9h1s7jb72ssnbvr376gs0vgds.apps.googleusercontent.com'
	client_secret='BaHkkaBxYk9d_b6cHE2iYGQ6'
	scope='https://www.googleapis.com/auth/admin.directory.device.chromeos')

service = build('admin', 'directory_v1')

class MainPage(webapp2.RequestHandler):

	@decorator.oauth_required
	def get(self):  
    	self.response.write(...)


class GetData(webapp2.RequestHandler):
	
	print 'Starting'
	@decorator.oauth_aware
	def post(self):
		if decorator.has_credentials():
			request = service.chromeosdevices().list(customerId='my_customer').execute()
			self.response.write(json.dumps(request))
		else:
			self.response.write(json.dumps({'error' : 'No credentials'}))

application = webapp2.WSGIApplication( [ 
	( '/', MainPage),
	('/get-data' GetData),
	(decorator.callback_path, decorator.callback_handler())
], debug=True )