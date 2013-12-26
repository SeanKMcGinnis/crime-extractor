import urllib2
import json
import logging
## Requires the Pyshp module available at: https://pypi.python.org/pypi/pyshp#downloads
import shapefile

## Variable definition
# Run in debug mode?
isDebug = False
url = 'http://www.crimemapping.com/GetIncidents.aspx?db=12/17/2013+00:00:00&de=12/23/2013+23:59:00&ccs=AR,AS,BU,DP,DR,DU,FR,HO,VT,RO,SX,TH,VA,VB,WE&xmin=-11887295.546046117&ymin=4167690.748278573&xmax=-11852077.18526377&ymax=4181965.36331081'
outPath = '../data/incidents'

w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field('AgencyID')
w.field('AgencyName')
w.field('CaseNumber')
w.field('CrimeCodeID')
w.field('CrimeCode')
w.field('DateReported')
w.field('Description')
w.field('Location')
w.field('X')
w.field('Y')
## TODO: Build the projection file

response = urllib2.urlopen(url).read()
data = json.loads(response.decode('utf8'))
incidents = data['incidents']
	
for incident in incidents:
	#logging.warning(incident['CrimeCode'])
	w.point(incident['X'], incident['Y'])
	w.record(incident['AgencyID'],incident['AgencyName'], incident['CaseNumber'],incident['CrimeCodeID'],incident['CrimeCode'],incident['DateReported'],incident['Description'],incident['Location'], incident['X'],incident['Y'])
	
w.save(outPath)

def getPRJ(epsg):
	"""
	Grab an WKT version of an EPSG code
	usage getPRJwkt(4326)
	"""
	f=urllib2.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg))
	return (f.read())