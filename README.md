#Chrome Device Manager

**Use OAuth 2.0 to download a device manifest for a domain using the [Admin SDK](https://developers.google.com/admin-sdk/directory/v1/guides/manage-chrome-devices) published by Google.**

Pages should allow user to view a CSV, or a detailed listing of the more pertinent information available to the Chrome Devices. Future releases may allow for editing of the updatable fields using the same API.
- - - 

##Top Priority

* Allow for separate download page of CSV
	* main page will explain whats going on, maybe make the API call and then allow for a button to download the actual CSV
* create usage stats and display on the 'main page'

- - -
## Low[er] Priority

### General Issues

* chromebooks don't save the page with a .csv ending
	* may have to create special URL handling for something like `/make.csv`
	* can manually edit file on fileshelf

### Logging
* Need good way to log entries, turn debug logging on / off
* Create a handy file for importing JSON data for local testing with python code
	* [Sample raw JSON gist](https://gist.github.com/ottiferous/5807894)

### Jinja2
* How many records to display per page?
* Update page with search
	* 	does this work on the entire blob or just the page?

### Templates
* Using [Twitter Bootstrap](http://twitter.github.io/bootstrap/)
