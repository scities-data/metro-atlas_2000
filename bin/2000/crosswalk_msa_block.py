"""crosswalk_msa_block.py

Extract the crosswalk between 2000 msa and blocks
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
blocks = []
for st in states:
    path = 'data/2000/shp/states/%s/blocks.shp'%st
    with fiona.open(path, 'r', 'ESRI Shapefile') as f:
        blocks.append(f['properties']['BLKIDFP00'])



#
# Group by MSA
#
msa_group = {}
for b in groups:
    county = b[:5]
    if county in county_to_msa:
        msa = county_to_msa[county]
        if msa not in msa_group:
            msa_group[msa] = []
        msa_group[msa].append(b)




#
# Save the crosswalk 
#
with open('data/2000/crosswalks/msa_block.csv', 'w') as output:
    output.write('MSA FIP\tBLOCK FIP\n')
    for msa in msa_block:
        ## Remove duplicates
        bs = list(set(msa_block[msa]))
        for b in bs:
            output.write('%s\t%s\n'%(msa, b))
