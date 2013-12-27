import urllib2
import json
import logging
from datetime import date, timedelta
from time import localtime, strftime
## Requires the Pyshp module available at: https://pypi.python.org/pypi/pyshp#downloads
import shapefile

## Agency ID
aid = 'b9663a24-c170-4f73-a490-ea4b0766b04d'
## Spatial Extent to filter the query
xmin = '-8340483.668819208'
ymin = '4892562.196762973'
xmax = '-8305265.30803686'
ymax = '4907123.450651281'
## Crime codes to query for
ccs = 'AR,AS,BU,DP,DR,DU,FR,HO,VT,RO,SX,TH,VA,VB,WE'
## Outpath and shapefile name
outPath = '../data/incidents'
## Number of Days for query
days = 90

## End Date for Query
yesterday = date.today() - timedelta(1)
## Start Date & Time for Query
sd = date.today() - timedelta(days)
db = sd.strftime('%m/%d/%Y') +'+00:00:00'
## End Date & Time for Query
de = yesterday.strftime('%m/%d/%Y') +'+23:59:59'


url = 'http://www.crimemapping.com/GetIncidents.aspx?db='+ db +'&de='+ de +'&ccs='+ccs+'&xmin='+xmin+'&ymin='+ymin+'&xmax='+xmax+'&ymax='+ymax +'&aid='+aid


w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field('AgID')
w.field('AgName')
w.field('CaseNum')
w.field('CrimeID')
w.field('CrimeCode')
w.field('DateRpt')
w.field('Desc','C','255')
w.field('Loc')
w.field('X')
w.field('Y')
## TODO: Build the projection file

try:
	response = urllib2.urlopen(url).read()
	data = json.loads(response.decode('utf8'))
	incidents = data['incidents']
	
	for incident in incidents:
		w.point(incident['X'], incident['Y'])
		w.record(incident['AgencyID'],incident['AgencyName'], incident['CaseNumber'],incident['CrimeCodeID'],incident['CrimeCode'],incident['DateReported'],incident['Description'],incident['Location'], incident['X'],incident['Y'])
		
	w.save(outPath)
except HTTPError, e:
	print 'The server couldn\'t fufill the request. Error Code: ', e.code
except URLError, e:
	print 'The server couldn\'t be reached. Error Code: ', e.code
	
def getPRJ(epsg):
	"""
	Grab an WKT version of an EPSG code
	usage getPRJwkt(4326)
	"""
	f=urllib2.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg))
	return (f.read())