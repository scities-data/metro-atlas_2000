""" tracts.py

Output one shapefile per MSA containing all the blockgroups it contains
"""
import os
import csv
import fiona


#
# Import MSA to tracts crosswalk 
#
msa_to_tract = {}
with open('data/crosswalks/msa_tracts.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa = rows[0]
        tract = rows[1]
        if msa not in msa_to_tract:
            msa_to_tract[msa] = []
        msa_to_tract[msa].append(tract)



#
# Perform the extraction
#
for n,msa in enumerate(msa_to_tract):
    print "Extract tracts for %s (%s/%s)"%(msa,
                                        n+1,
                                        len(msa_to_tract))
    states = list(set([b[:2] for b in msa_to_tract[msa]]))

    ## Get all blockgroups
    all_tract = {}
    for st in states:
        with fiona.open('data/shp/state/%s/tracts.shp'%st, 'r',
                'ESRI Shapefile') as source:
            source_crs = source.crs
            for f in source:
                all_tract[f['properties']['CTIDFP00']] = f['geometry']

    ## blockgroups within cbsa
    msa_tract = {tract: all_tract[tract] for tract in msa_to_tract[msa]}

    ## Save
    if not os.path.isdir('data/shp/msa/%s'%msa):
        os.makedirs('data/shp/msa/%s'%msa)

    path = 'data/shp/msa/%s/tracts.shp'%msa
    schema = {'geometry': 'Polygon',
              'properties': {'CTIDFP00': 'str'}}
    with fiona.open(path, 'w','ESRI Shapefile',
                            crs = source_crs,
                            schema = schema) as output:
        for tract in msa_tract:
            rec = {'geometry':msa_tract[tract], 'properties':{'CTIDFP00':tract}}
            output.write(rec)
