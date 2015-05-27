"""shape_msa_county.py

Output one shapefile per MSA containing all the counties it contains
"""
import os
import csv
import fiona


#
# Import MSA to blockgroup crosswalk 
#
msa_to_county = {}
with open('data/2000/crosswalks/msa_county.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa = rows[0]
        county = rows[1]
        if msa not in msa_to_county:
            msa_to_county[msa] = []
        msa_to_county[msa].append(county)



#
# Perform the extraction
#
print "Extract counties for all MSAs in the US"

## Get all blockgroups
all_county = {}
with fiona.open('data/2000/shp/us/counties.shp', 'r',
        'ESRI Shapefile') as source:
    source_crs = source.crs
    for f in source:
        all_county[f['properties']['CNTYIDFP00']] = f['geometry']

for n,msa in enumerate(msa_to_county):
    print "Extract counties for %s (%s/%s)"%(msa,n+1,len(msa_to_county))

    ## blockgroups within cbsa
    msa_county = {county: all_county[county] for county in msa_to_county[msa]}

    ## Save
    if not os.path.isdir('data/2000/shp/msa/%s'%msa):
        os.makedirs('data/2000/shp/msa/%s'%msa)

    schema = {'geometry': 'Polygon',
              'properties': {'CNTYIDFP00': 'str'}}
    with fiona.open('data/2000/shp/msa/%s/counties.shp'%msa, 'w', 
            'ESRI Shapefile',
            crs = source_crs,
            schema = schema) as output:
        for county in msa_county:
            rec = {'geometry':msa_county[county], 'properties':{'CNTYIDFP00':county}}
            output.write(rec)
