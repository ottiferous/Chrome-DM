#Chrome Device Manager

**Use OAuth 2.0 to download a device manifest for a domain using the [Admin SDK](https://developers.google.com/admin-sdk/directory/v1/guides/manage-chrome-devices) published by Google.**

Pages allow user to download a CSV, or an abridged listing of the more basic information on the devices. A top section will outline basic useful information found from the device manifest.

	Sample statistics will include (percentage and numbers should be available)

	- Devices on current / any reported version(s)
	- Devices that have synced within the last 7 days
	- Number of devices in each OU

Future releases may allow for editing of the updatable fields inline. 


- - - 

##Top Priority

* Create usage stats and display on the 'main page'
	* Use HTML5 javascsript charts with `canvas` objects
	* [ChartJS](http://www.chartjs.org/docs/)
* Develop more robust unit tests

- - -
## Low[er] Priority

### General Issues

* Fix full page `div` for the `Download CSV` button
	* should be slightly larger than button

### Logging
* Need good way to log entries, turn debug logging on / off
* Create a handy file for importing JSON data for local testing with python code
	* [Sample raw JSON gist](https://gist.github.com/ottiferous/5807894)

### Jinja2
* How many records to display per page?
* Update page with search
	* 	does this work on the entire blob or just the page?
* Headers are not in sync with dictionary elements - keep an eye on that
	*  looks like `dict` objects don't preserve order. Reversing logic in `BuildChromeManifest` may fix this

### Templates
* Using [Twitter Bootstrap](http://twitter.github.io/bootstrap/)
