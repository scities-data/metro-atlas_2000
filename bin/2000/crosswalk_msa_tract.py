"""crosswalk_msa_tract.py

Extract the crosswalk between 2000 msa and tracts.
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


## Import all tracts ids
tracts = []
for st in states:
    path = 'data/2000/shp/states/%s/tracts.shp'%st
    with fiona.open(path, 'r', 'ESRI Shapefile') as f:
        tracts.append(f['properties']['CTIDFP00'])



#
# Group by MSA
#
msa_tract = {}
for tr in tracts:
    county = tr[:5]
    if county in county_to_msa:
        msa = county_to_msa[county]
        if msa not in msa_tract:
            msa_tract[msa] = []
        msa_tract[msa].append(tr)




#
# Save the crosswalk 
#
with open('data/2000/crosswalks/msa_tract.csv', 'w') as output:
    output.write('MSA FIP\tTRACT FIP\n')
    for msa in msa_tract:
        ## Remove duplicates
        trs = list(set(msa_tract[msa]))
        for tr in trs:
            output.write('%s\t%s\n'%(msa, tr))
