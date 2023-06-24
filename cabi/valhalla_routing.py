# %%
import geopandas as gpd
import pandas as pd
from numpy import array_split
from itertools import islice
from sqlalchemy import create_engine
from tqdm import tqdm
from shapely.geometry import LineString
import numpy as np
from valhalla import Actor, get_config, get_help
from valhalla.utils import decode_polyline
from logzero import logger

import time
import sys
import warnings

# setup the default database parameters
DATABASE_NAME = 'cabidb'
USERNAME = 'admin'
PASSWORD = 'maxpass'

# create a postgis database connection
engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@127.0.0.1:5432/{DATABASE_NAME}")

# ignore annoying warnings
sys.warnoptions = "ignore"
warnings.simplefilter("ignore")

# Load the Valhalla configuration
config = get_config("./data/osm_data/valhalla_tiles.tar", verbose=False)
actor = Actor(config)


def combine_trips_with_geom():
    """
    This function combines trip information and station information to return a merged dataframe with columns for
    start and end latitudes, start and end longitudes, and the popularity of the trip.
    
    Returns:
        mergedf (pd.DataFrame): a dataframe with columns for start and end latitudes, start and end longitudes, and 
        the popularity of the trip
    """
    # load the dataframe of route popularity
    pairs = pd.read_csv("./data/processed/route_stats.csv")
    # load the stations
    stations = pd.read_csv(
        "./data/processed/stationLookup.csv", index_col="short_name"
    )
    # get a list of the stations we already have in the PostGIS db
    existing_routes_df = pd.read_sql_query("select st,en from route_geometry", engine)

    station_combo_list = (
        existing_routes_df.st.astype("str") + existing_routes_df.en.astype("str")
    ).astype("int64")
    # datframe of lat and long indexed by the station id
    lookup_series = stations.loc[:, ["lat", "lon"]]

    # we find new unique pairs not already in the database
    new_pairs = pairs[
        ~(pairs.st.astype("str") + pairs.en.astype("str"))
        .astype("int64")
        .isin(list(station_combo_list))
    ]

    # catch the case where there is nothing new
    if len(new_pairs) == 0:
        logger.info("No new station combos were found")
        return

    # if there is something new, print to the console
    logger.info(f"{len(new_pairs)} New station combinations were found in the data. They will be added to the routes table")

    # combine the stations and the route popularity, and make them into tuples of the latlongs
    mergedf = (
        new_pairs.merge(
            lookup_series,
            how="left",
            left_on="st",
            right_index=True,
            validate="m:1",
        )
        .rename(columns={"lon": "start_long", "lat": "start_lat"})
        .merge(
            lookup_series, how="left", left_on="en", right_index=True, validate="m:1"
        )
        .rename(columns={"lon": "end_long", "lat": "end_lat"})
    )

    return mergedf

def get_route_geometry(starty, startx, endy, endx, use_roads=0.1, use_hills=0.1):
    """Find a route in DC using valhalla

    Args:
        startx (float): starting longitude
        starty (float): starting latitude
        endx (float): ending longitude
        endy (float): ending latitude
        use_roads (float, optional): factor for how much road is allowed in the route. Defaults to 0.1.
        use_hills (float, optional): factor for how much hills are allowed in the route. Defaults to 0.1.

    Returns:
        LineString: Shapely linestring of the assumed route
        float: Time taken to complete the route
        float: Length of the route
    """
    # set up the routing parameters
    requeststring = {
        "locations": [{"lat": starty, "lon": startx}, {"lat": endy, "lon": endx}],
        "costing": "bicycle",
        "costing_options": {
            "bicycle": {
                "bicycle_type": "hybrid",
                "use_roads": use_roads,
                "use_hills": use_hills,
                "use_ferry": 0,
            }
        },
        "directions_type": "none",
    }
    # attempt routing and give a NaN if there is an issue
    try:
        response = actor.route(requeststring)
        # convert the encoded polyline into a format readable by shapely
        route_linestring, time, distance = process_routing_response(response)
        return route_linestring,time,distance
    except RuntimeError:
        return np.NaN, np.NaN, np.NaN


def process_routing_response(response):
    """Extract data from the routing response

    Args:
        response (dict): The routing response from the valhalla API

    Returns:
        LineString: Shapely linestring of the assumed route
        time (int): Time required to traverse the route
        length (int): Length of the route in meters
    """
    # Extract the encoded polyline string from the response
    polyline_enc = response["trip"]["legs"][0]["shape"]
    # Decode the encoded polyline into a format readable by shapely
    polyline_dec = decode_polyline(polyline_enc)
    # Extract the time required to traverse the route from the response
    triptime = response["trip"]["legs"][0]["summary"]["time"]
    # Extract the length of the route in meters from the response
    length = response["trip"]["legs"][0]["summary"]["length"]
    # Return the decoded polyline as a shapely linestring, the time and the length
    return LineString(polyline_dec), triptime, length


def insert_into_postgis(df_chunk):
    chunklen = len(df_chunk)
    tqdm.write(f'routing chunk {chunklen} trips')
    geomlist = []
    timelist = []
    distlist = []
    starttime = time.perf_counter()
    for starty, startx, endy, endx in df_chunk.iloc[:, 3:].values:
        geometry, triptime, distance = get_route_geometry(starty, startx, endy, endx)
        geomlist.append(geometry)
        timelist.append(triptime)
        distlist.append(distance)
    t_after_routing = time.perf_counter()
    routing_time = t_after_routing - starttime
    tqdm.write(f"Routed {chunklen} trips in {routing_time:.2f} seconds ({routing_time/chunklen:.3f} s/trip)")
    sql_insert_chunksize = 100
    gpd.GeoDataFrame(df_chunk).drop(
            columns=["start_lat", "start_long", "end_lat", "end_long", "popularity"]
        ).assign(
            triptime=timelist, tripdist=distlist, geom=geomlist
        ).dropna().set_geometry(
            "geom", crs="EPSG:4326"
        ).to_crs(
            "EPSG:26985"
        ).to_postgis(
            "route_geometry", con=engine, if_exists="append", index=False,chunksize=sql_insert_chunksize
        )
    t_after_insert = time.perf_counter()
    inserttime = t_after_insert-t_after_routing
    tqdm.write(f'Sucessfully loaded trips into PostGIS in {inserttime:.2f} seconds in subbatches of {sql_insert_chunksize} rows ({inserttime/chunklen:.3f} s/trip)')

def split_dataframe(df,chunk_size):
    return [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]


def main():
    mergedf = combine_trips_with_geom()
    if mergedf is None:
        return 0
    
    # this is rather arbitrarily done in 200 chunks
    for chunk in tqdm(split_dataframe(mergedf, 500)):
        insert_into_postgis(chunk)


# %%
if __name__ == "__main__":
    main()

# %%
