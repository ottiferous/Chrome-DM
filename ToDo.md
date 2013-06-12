# Parsing JSON data from Chrome

#### General Cleanup
1. remove empty lines
2. remove header info

#### Begin Parsing Objects
3. find header for each object
	* Try `"kind": "admin#directory#chromeosdevice""` entry
4. create dict / tuple based on the key values
	* account for missing values `for _ in data:`
5. append each object to a new `Chrome_Manifest` array

#### Misc
* check for invalid characters in `notes`, `usernames`, and `location`
	* could cause improper parsing if not careful
	* use a 1-entry per line approach

#### Output Styles
* CSV
	* how do you handle `,` in notes when exporting?
* Plaintext file
* HTML page