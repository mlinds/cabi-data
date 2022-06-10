#!/bin/sh
sudo apt install osmctools -y
osmconvert ..data/osm_data/states/district-of-columbia-latest.osm.pbf --out-o5m -b=-77.3724,38.7685,-76.8474,39.1599 \
 | osmconvert - ..data/osm_data/states/maryland-latest.osm.pbf --out-o5m -b=-77.3724,38.7685,-76.8474,39.1599 \
 | osmconvert - ..data/osm_data/states/district-of-columbia-latest.osm.pbf -b=-77.3724,38.7685,-76.8474,39.599 -o=all_dc_area.pbf