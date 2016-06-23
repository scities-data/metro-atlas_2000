""" us.py

Output one shapefile for the entire US (MultiPolygon).
"""
import os
import csv
import fiona
from shapely.ops import cascaded_union
from shapely.geometry import mapping, shape



#
# Perform the extraction
#
print "Merge the US features."



#
# Import the unmerged US shapefile
#
all_us = {}
with fiona.open('data/shp/us/us_unmerged.shp', 'r',
        'ESRI Shapefile') as source:
    source_crs = source.crs
    for f in source:
        all_us[f['properties']['NATION010']] = shape(f['geometry'])

us_boundary = cascaded_union(all_us.values())



#
# Save the merged features
#
schema = {'geometry': 'Polygon',
          'properties': {'NATION010': 'str'}}
with fiona.open('data/shp/us/us.shp', 'w', 
        'ESRI Shapefile',
        crs = source_crs,
        schema = schema) as output:
    if us_boundary.geom_type == 'Polygon':
        rec = {'geometry':mapping(us_boundary), 'properties':{'NATION010': 'US'}}
        output.write(rec)
    elif us_boundary.geom_type == 'MultiPolygon':
        for bd in us_boundary:
            rec = {'geometry':mapping(bd), 'properties':{'NATION010':'US'}}
            output.write(rec)
    else:
        print 'Error'
