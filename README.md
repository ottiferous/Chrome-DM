# Introduction

## Background
Currently there is a lack of accessible information for Enterprise Hardware. Over half of the fields are not available using the Chrome Management dashboard, and exporting device information (serial numbers, user, location, OU, etc.) is absent. This leaves customers with large numbers of devices unable to manage an enterprise fleet of Chromebooks.

Leveraging available APIs to retrive information about all Chromebooks enrolled to a domain the application will be able to aggregate all of the available information for admins into a lightweight CSV. 

## Design Goals
Existing on the Google AppEngine cloud platform allows for scalability and accessiblity across all users of the Enterprise Management feature of Google Apps with Chrome devices. Keeping the code in a central location prevents the need to install and run the source code locally.

As patterns emerge additional information can be shown to highlight the current 'health' of enrolled devices. To alleviate any security concerns the tool will make use of existing 3-legged OAuth services from Google. To encourage adoption and extensibility the source-code is available on Github.

---

# Architecture

## Introduction
This allows running independent of platform. To execute an API query the tool assumes that:

* the domain has enabled API access
* admin credentials are supplied

Google takes care of the authentication removing the need to store credentials locally.

The UI is composed of a web-page hosted on AppEngine. The higher number of API queries using this method of caching system is believed to be negligible.


## Data
Data will take three main forms during a session: JSON, a __dict__ object, and CSV.

#### JSON
The JSON file is the response from an API query made against a domain wtih Chrome Devices / Management. This data is ingested using the __BuildChromeManifest__ method to turn the data into a useful form for getting information.

###### Sample JSON response
Edited for readabiliy

```
{
	u'status': 				u'ACTIVE', 
	u'lastSync': 			u'2013-01-16T23:52:13.487Z', 
	u'kind': 				u'admin#directory#chromeosdevice', 
	u'lastEnrollmentTime': 	u'2013-01-16T23:46:04.757Z', 
	u'serialNumber': 		u'HY3A91ECB17898',
	u'deviceId': 			u'ca34540c-ede5-4529-88b5-9b3214737db6', 
	u'orgUnitPath': 		u'/'
}
```
#### Python Dict
Follows the same format as the JSON response above. The JSON response is already in a python dict format.

#### CSV
The last format for the data will be as a CSV containing the API response. Some information may be stripped in the transition to CSV, namely the decorator and JSON descriptor fields as the type of object is clearly assumed to be a Chrome Device at this point.

###### Sample CSV output
```
"ACTIVE"," "," "," ","2013-01-16T23:46:04.757Z"," "," ","HY3A91ECB17898"," "," "," "," "," ","ca34540c-ede5-4529-88b5-9b3214737db6","2013-01-16T23:52:13.487Z"," ","/"," "," "
```

## Database
The design can be done without a database. The need for a database is centered around gathering information with specific OU's. Using a database will allow for easily gathering the necessary records from large API responses. The overhead will be negligible for smaller domains; medium-to-larger-sized domains that do not make use of OU's will experience the most slowdown due to the added overhead of ingestion.

### Schema
The schema will follow that of the JSON response. Each Table will have fields for every entry within the JSON response and map them in a 1:1 fashion. The previously mentioned entires will be omitted.

## Code

### Introduction
Python was chosen because of the __OAuth2Decorator__ class that is made available. This kept the barrier to entry as low as possible to get CDM started. Python is also the preferred language of the development team that is available on AppEngine. A template-engine, Jinja, is used to dynamically render the HTML pages for stats and general information gathered from teh API responses.

### Modules

![Workflow](http://i.imgur.com/Su5rMa3.png "Workflow")
#### Google
The OAuth decorator and httplib files were gathered from the Google Developer site. These are not maintained by this project and are assumed to be stable.

#### Hortator
Is responsible for most of the data manipulation methods. Connects the View to the API Data.

#### Jinja
Responsible for rendering the HTML pages and filling in the data gathered from __Hortator__. Handles all URL requests.

#### Internal Functions

###### GetChromeManifest
Takes a single argument of type OAuth2Decorator and uses this to creates the necessary object for making the appropriate API call.

###### BuildChromeManifest
Takes a template and the results from __GetChromeManifest__ to map the information across devices to a new returned dictionary object.

###### StatsFromManifest
Runs analysis on final form of manifest to get usage and sync statistics for displaying in the summary view. Returns a dictionary object with the results from the queries.


---

# Operation
Information will be displayed as a summary view for the entire domain so a 'general health' of the devices can be determined. A CSV download will enable more detailed queries with 3rd party spreadsheet / database applications.

### First time use
On visiting the __/stats__ page for a user who is not currently logged in they will trigger the 3-legged OAuth flow. A login page from Google is shown to allow authentication. Once credentials have been verified the API call will be made and results passed along to the rendering engine - Jinja.

Here users will be able to see the stats displayed and click on a button to download the entire device listing as a CSV file.

### Users without API service
The 3-legged OAuth will trigger like any other user - but they will get a 400 error when the API call is made. This will cause a new page to be shown with the error message and links to possible solutions - like enabling API access for the domain.

---

## Licensing
The source code for this project is provided for use under the [MIT license](https://github.com/ottiferous/Chrome-DM/blob/master/MIT%20License.txt)
