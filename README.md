#Chrome Device Manager

**Use OAuth 2.0 to download a device manifest for a domain using the [Admin SDK](https://developers.google.com/admin-sdk/directory/v1/guides/manage-chrome-devices) published by Google.**

Pages should allow user to view a CSV, or a detailed listing of the more pertinent information available to the Chrome Devices. Future releases may allow for editing of the updatable fields using the same API.
- - - 
##Top Priority

* ~~account for empty values~~
   * ~~replace `''` with `' '` or other value.~~
	   * ~~map(lambda) works well~~
* allow for separate download page
	* main page will explain whats going on, maybe make the API call and then allow for a button to download the actual CSV
	* ~~remove unnecessary / unwanted fields~~
		* ~~kind, model, etc.~~
* keep `dict` data type for more dynamic page rendering
	* allows for custom views to always be in right order by basing colum off of key value instead of order 

- - -

## Miscellaneous

### General Issues

* chromebooks don't save the page with a .csv ending
	* may have to create special URL handling for something like `/make.csv`
	* can manually edit file on fileshelf
* Main landing page
	* JINJA2 template or static HTML?

### Logging
* Need good way to log entries, turn debug logging on / off
* Create a handy file for importing JSON data for local testing with python code
	* [Sample raw JSON gist](https://gist.github.com/ottiferous/5807894)

### Jinja2

* ~~Find current version and edit app.yaml~~
* ~~Rendering device list~~
	* render all on one page?
	* 20 per page? User setting?
* Update page with search
	* 	does this work on the entire blob or just the page?
* render with nested for loops?

		<tbody>
			{% for row in device_page %}
				<tr>
					{% for entry in row %}
						<td> entry </td>
					{% endfor %}
				</tr>
			{% endfor %}
		</tbody>`
This is frowned on - and will probably be super slow when it comes to anything over 20 items. Find cleaner way to do this…

### Templates
* Using [Twitter Bootstrap](http://twitter.github.io/bootstrap/)
* Is there a [Google bootstrap](http://todc.github.io/todc-bootstrap/)?