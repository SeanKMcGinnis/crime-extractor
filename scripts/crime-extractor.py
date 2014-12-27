import os
import urllib2
import json
import logging
from datetime import date, timedelta
from time import localtime, strftime
## Requires the Pyshp module available at: https://pypi.python.org/pypi/pyshp#downloads
import shapefile

def createIncidents(objShp):
    ## Get the incidents
    incidents = makeRequest()
    ## Iterate through the results and add them to the SHP
    for incident in incidents:
        ## Create the point
        objShp.point(float(incident['Y']), float(incident['X']), 0, 0)
        ## Add the attributes
        objShp.record(incident['AgencyID'],incident['AgencyName'], incident['CaseNumber'],incident['CrimeCodeID'],incident['CrimeCode'],incident['DateReported'],incident['Description'],incident['Location'], incident['X'],incident['Y'])
    ## Save the shapefile
	objShp.save(outPathShp)

def updateIncidents():
    ## Create the editor object
    objShp = shapefile.Editor(outPathShp)
    ## Get the incidents
    incidents = makeRequest()
    ## Iterate through the results and add them to the SHP
    for incident in incidents:
        ## Create the point
        objShp.point(float(incident['Y']), float(incident['X']), 0, 0)
        ## Add the attributes
        objShp.record(incident['AgencyID'],incident['AgencyName'], incident['CaseNumber'],incident['CrimeCodeID'],incident['CrimeCode'],incident['DateReported'],incident['Description'],incident['Location'], incident['X'],incident['Y'])
        ## Save the new record
        objShp.save(outPathShp)

def makeRequest():
    ## build the response by querying the service
    response = urllib2.urlopen(url).read()
    ## parse the json to data
    data = json.loads(response.decode('utf8'))
    ## get down to the individual insidents
    return data['incidents']

## [Agency ID, Agency Name, XMin, YMin, XMax, YMax]
aids = [\
        ['b9663a24-c170-4f73-a490-ea4b0766b04d', 'Trenton','-8340483.668819208','4892562.196762973','-8305265.30803686','4907123.450651281'],\
        ['e9848f89-8aa2-4497-b074-060be11ea1f7','Phillipsburg','-8373996.686592114','4965725.991892121','-8364078.982172125','4970455.53301726']\
        ]
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
    ## Construct the url to query
    url = 'http://www.crimemapping.com/GetIncidents.aspx?db='+ db +'&de='+ de +'&ccs='+ccs+'&xmin='+aid[2]+'&ymin='+aid[3]+'&xmax='+aid[4]+'&ymax='+aid[5] +'&aid='+aid[0]
    ## Check to see if the SHP already exists
    if os.path.isfile(outPathShp+ '.shp'):
        ## If SHP exists, update it
        updateIncidents()
    else:
        ## If SHP does not exist, create it
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
        ## Pass it on to be populated
        createIncidents(w)
