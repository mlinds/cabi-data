#!/bin/sh
# wget http://download.geofabrik.de/north-america/us/virginia-latest.osm.pbf
# wget http://download.geofabrik.de/north-america/us/maryland-latest.osm.pbf
# wget http://download.geofabrik.de/north-america/us/district-of-columbia-latest.osm.pbf
sudo apt install osmctools -y
osmconvert ./states/virginia-latest.osm.pbf --out-o5m -b=-77.4,38.7,-76.7,39.2 | osmconvert - ./states/maryland-latest.osm.pbf --out-o5m -b=-77.4,38.7,-76.7,39.2 | osmconvert - ./states/district-of-columbia-latest.osm.pbf -b=-77.4,38.7,-76.7,39.2 -o=all_dc_area.pbf