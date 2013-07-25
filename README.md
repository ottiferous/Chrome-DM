#Chrome Device Manager

**Use OAuth 2.0 to download a device manifest for a domain using the [Admin SDK](https://developers.google.com/admin-sdk/directory/v1/guides/manage-chrome-devices)**

Allows for downloading a CSV, or viewing an abridged listing of the more basic information on the devices. A top section will outline basic useful information found from the API query. A sample API response can be seen [here](https://gist.github.com/ottiferous/5807894).

	Sample statistics include

	- Devices that have synced within the last 7 days
	- Total number of devices
	- Number of devices in each OU
	
	The following may be available ( depending on device state reporting )
	
	- Number of devices on each channel
	- Devices on each reported version

Future releases may allow for editing of the updatable fields inline. 


- - - 

##Top Priority

* Display stats using charts / graphics
	* Use HTML5 javascsript charts with `canvas` objects
	* [ChartJS](http://www.chartjs.org/docs/)
* Develop more robust unit tests
* Better Error handling
* Use template inheritance