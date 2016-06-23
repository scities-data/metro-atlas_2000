""" msa.py

Output one shapefile per MSA containing its boundaries.
"""
import os
import csv
import fiona
from shapely.ops import cascaded_union
from shapely.geometry import mapping, shape

#
# Import MSA to blockgroup crosswalk 
#
msa_to_county = {}
with open('data/crosswalks/msa_counties.csv', 'r') as source:
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
print "Extract the boundaries of MSAs in the US"


## Get all blockgroups
all_county = {}
with fiona.open('data/shp/us/counties.shp', 'r',
        'ESRI Shapefile') as source:
    source_crs = source.crs
    for f in source:
        all_county[f['properties']['CNTYIDFP00']] = shape(f['geometry'])

for n,msa in enumerate(msa_to_county):
    print "Extract and merge counties for %s (%s/%s)"%(msa,n+1,len(msa_to_county))

    ## blockgroups within cbsa
    msa_county = {county: all_county[county] for county in msa_to_county[msa]}
    msa_boundary = cascaded_union(msa_county.values())

    ## Save
    if not os.path.isdir('data/shp/msa/%s'%msa):
        os.makedirs('data/shp/msa/%s'%msa)

    schema = {'geometry': 'Polygon',
              'properties': {'MSAIDFP00': 'str'}}
    with fiona.open('data/shp/msa/%s/boundaries.shp'%msa, 'w', 
            'ESRI Shapefile',
            crs = source_crs,
            schema = schema) as output:
        if msa_boundary.geom_type == 'Polygon':
            rec = {'geometry':mapping(msa_boundary), 'properties':{'MSAIDFP00':msa}}
            output.write(rec)
        elif msa_boundary.geom_type == 'MultiPolygon':
            for bd in msa_boundary:
                rec = {'geometry':mapping(bd), 'properties':{'MSAIDFP00':msa}}
                output.write(rec)
        else:
            print 'Error'
