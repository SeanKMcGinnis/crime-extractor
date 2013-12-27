crime-extractor
===============

Python script to scrape crime information from <a href="http://www.crimemapping.com">CrimeMapping.com</a>

The script takes the variables, builds the request and converts the JSON response into a shapefile

Dependencies
===========
Python 2.7 (It might work in other version, I have only tested in 2.7)
<a href="https://code.google.com/p/pyshp/">pyshp</a> - Python Shapefile Library

Variables
===========
aid - Agency ID
xmin - 
ymin
xmax
ymax
ccs
outpath
days

Known Limitations
===========
* The GetIncidents page will return 800 incidents at a time given, need to come up with away to break requests into smaller time chunks when more than 800 incidents exist

In Process Functionality
===========
* Requesting extent information from CrimeMapping.com Agency Information page
* Scraping incident information from <a href="http://www.crimereports.com>CrimeReports.com</a>
* 
