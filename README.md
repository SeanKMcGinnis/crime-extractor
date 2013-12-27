crime-extractor
===============

Python script to scrape crime information from <a href="http://www.crimemapping.com">CrimeMapping.com</a>

The script takes the variables, builds the request and converts the JSON response into a shapefile

<strong>Dependencies</strong><br />
* Python 2.7 (It might work in other version, I have only tested in 2.7)
* <a href="https://code.google.com/p/pyshp/">pyshp</a> - Python Shapefile Library

<strong>Variables</strong><br />
* aid - Agency ID to filter results for a specific agency
* xmin - Minimum X value for search extent
* ymin - Minimum Y value for search extent
* xmax - Maximum X value for search extent
* ymax - Maximum Y value for search extent
* ccs - Crime codes, check wiki for list of valid codes
* outpath - path to save output shapefile
* days - days of incident history

<strong>Known Limitations</strong><br />
* The GetIncidents page will return 800 incidents at a time given, need to come up with away to break requests into smaller time chunks when more than 800 incidents exist

<strong>In Process Functionality</strong><br />
* Requesting extent information from CrimeMapping.com Agency Information page
* Scraping incident information from <a href="http://www.crimereports.com>CrimeReports.com</a>
