"""crosswalk_msa_blockgroup.py

Extract the crosswalk between 2000 msa and blockgroups
"""
import os
import csv
import fiona

#
# Import data
#

## MSA to counties crosswalk
# county_to_msa = {county: {msa: [cousub ids]}
county_to_msa = {}
with open('data/2000/crosswalks/msa_county.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        county = rows[1]
        msa = rows[0]
        county_to_msa[county] = msa


## Import list of states
states = []
with open('data/state_numbers.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        states.append(rows[0])


## Import all blockgroup ids
blockgroups = []
for st in states:
    path = 'data/2000/shp/states/%s/blockgroups.shp'%st
    with fiona.open(path, 'r', 'ESRI Shapefile') as f:
        blockgroups.append(f['properties']['BKGPIDFP00'])



#
# Group by MSA
#
msa_blockgroup = {}
for bg in blockgroups:
    county = bg[:5]
    if county in county_to_msa:
        msa = county_to_msa[county]
        if msa not in msa_blockgroup:
            msa_blockgroup[msa] = []
        msa_blockgroup[msa].append(bg)




#
# Save the crosswalk 
#
with open('data/2000/crosswalks/msa_blockgroup.csv', 'w') as output:
    output.write('MSA FIP\tBLOCKGROUP FIP\n')
    for msa in msa_blockgroup:
        ## Remove duplicates
        bgs = list(set(msa_blockgroup[msa]))
        for bg in bgs:
            output.write('%s\t%s\n'%(msa, bg))
