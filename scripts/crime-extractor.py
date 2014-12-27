import os
import urllib2
import json
import logging
from datetime import date, timedelta
from time import localtime, strftime
## Requires the Pyshp module available at: https://pypi.python.org/pypi/pyshp#downloads
import shapefile

def createIncidents(objShp):
    incidents = makeRequest()
    buffer = []
    for incident in incidents:
        objShp.point(float(incident['Y']), float(incident['X']), 0, 0)
        objShp.record(incident['AgencyID'],incident['AgencyName'], incident['CaseNumber'],incident['CrimeCodeID'],incident['CrimeCode'],incident['DateReported'],incident['Description'],incident['Location'], incident['X'],incident['Y'])

    ## Save the shapefile
	objShp.save(outPathShp)

def updateIncidents():
    objShp = shapefile.Editor(outPathShp)
    incidents = makeRequest()
    for incident in incidents:
        objShp.point(float(incident['Y']), float(incident['X']), 0, 0)
        objShp.record(incident['AgencyID'],incident['AgencyName'], incident['CaseNumber'],incident['CrimeCodeID'],incident['CrimeCode'],incident['DateReported'],incident['Description'],incident['Location'], incident['X'],incident['Y'])
        objShp.save(outPathShp)

def makeRequest():
    response = urllib2.urlopen(url).read()
    data = json.loads(response.decode('utf8'))
    return data['incidents']

def buildGeoJSON(outPath):
    return open(outPath + '.json', 'w')


## Agency ID
aids = [['b9663a24-c170-4f73-a490-ea4b0766b04d', 'Trenton']]
## Spatial Extent to filter the query
xmin = '-8340483.668819208'
ymin = '4892562.196762973'
xmax = '-8305265.30803686'
ymax = '4907123.450651281'
## Crime codes to query for
ccs = 'AR,AS,BU,DP,DR,DU,FR,HO,VT,RO,SX,TH,VA,VB,WE'

## Number of Days for query
days = 7

## End Date for Query
yesterday = date.today() - timedelta(1)
## Start Date & Time for Query
sd = date.today() - timedelta(days)
db = sd.strftime('%m/%d/%Y') +'+00:00:00'
## End Date & Time for Query
de = yesterday.strftime('%m/%d/%Y') +'+23:59:59'

for aid in aids:
    ## Outpath and shapefile name
    outPathShp = '../data/shp/incidents' + aid[1]
    url = 'http://www.crimemapping.com/GetIncidents.aspx?db='+ db +'&de='+ de +'&ccs='+ccs+'&xmin='+xmin+'&ymin='+ymin+'&xmax='+xmax+'&ymax='+ymax +'&aid='+aid[0]

    if os.path.isfile(outPathShp+ '.shp'):
        print('Exists')
        updateIncidents()
    else:
        print('Create')
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
        createIncidents(w)
