# Makefile
# misusing make for things its not intended for
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables
MAKEFLAGS += --warn-undefined-variables

# Define the Python interpreter
PYTHON = python

# Define the files that trigger the rebuild
DATA_FILES := $(wildcard data/tripdata/*.csv) data/processed/stationLookup.csv

all: cabi/load_csv_trips.py data/interim/comb_trips.gzip data/processed/route_stats.csv data/processed/station_stats.csv cabi/valhalla_routing.py

cabi/load_csv_trips.py: cabi/tripio.py
	touch cabi/load_csv_trips.py

data/interim/comb_trips.gzip: $(DATA_FILES) cabi/load_csv_trips.py 
	$(PYTHON) cabi/load_csv_trips.py

data/processed/route_stats.csv: data/interim/comb_trips.gzip cabi/update_route_statistics.py
	$(PYTHON) cabi/update_route_statistics.py

data/processed/station_stats.csv: cabi/update_station_statistics.py data/interim/comb_trips.gzip
	$(PYTHON) cabi/update_station_statistics.py

#we don't have a good way to check the database write happened so touch this file to mark that
cabi/valhalla_routing.py: data/osm_data/valhalla_tiles.tar data/processed/route_stats.csv data/processed/stationLookup.csv
	$(PYTHON) cabi/valhalla_routing.py
	touch cabi/valhalla_routing.py

