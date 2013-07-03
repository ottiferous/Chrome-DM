### General Issues

* chromebooks don't save the page with a .csv ending
	* may have to create special URL handling for something like `/make.csv`
	* can manually edit file on fileshelf
* Create main landing page
	* JINJA2

### Jinja

* Find current version and edit app.yaml
* Rendering device list
	* render all on one page?
	* 20 per page? User definable?
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

### Template
* Is there a Google bootstrap?