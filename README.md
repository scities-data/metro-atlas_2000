# US Metropolitan atlas 2000

Provides an Atlas of the US Metropolitan areas geographies for the 2000 US
Census. Inspired by Mike Bostock's [us-atlas](https://github.com/mbostock/us-atlas).

## Features available

Data tabulation geographical levels:

* Census Blocks boundaries (blocks)
* Census Block Groups boundaries (blockgroups)
* Census Tracts boundaries (tracts)
* Counties boundaries (countries)

## Use

In the commande line, go in the folder where you cloned the repository, and type
(to get the blockgroups)

```bash
make blockgroups
```

The program will download the necessary data, and the shapefiles will be
available in the folder `data/shp/msa_id/`

## License

The code is distributed under the BSD License.
