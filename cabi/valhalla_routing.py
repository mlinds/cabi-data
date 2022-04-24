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

engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/pgrouting_data")
#%%

config = get_config('../data/osm_data/valhalla_tiles.tar',verbose=False)
actor = Actor(config)

# tool that queries the running instance of valhalla
def get_route(startx, starty, endx, endy):
    """Find a route in DC using valhalla

    Args:
        startx (float): starting longitude
        starty (float): starting latitude
        endx (float): ending longitude
        endy (float): ending latirude

    Returns:
        LineString: Shapeley linestring of the assumed route
    """    
    # set up the routing parameters
    requeststring = {
        "locations": [{"lat":starty,"lon":startx},{"lat":endy,"lon":endx}],
        "costing":"bicycle",
        "costing_options": {
            "bicycle": {
                "bicycle_type": "hybrid",
                "use_roads": 0.1,
                "use_hills": 0.1,
                "use_ferry": 0,
            }
        },
        "directions_type":"none"
    }
    # attempt routing and give a NaN if there is an issue
    try: 
        response = actor.route(requeststring)
        polyline_enc = response['trip']['legs'][0]['shape']
        polyline_dec = decode_polyline(polyline_enc)
        return LineString(polyline_dec)
    except RuntimeError:
        print(f'{(startx, starty, endx, endy)} couldnt be routed')
        return np.NaN

def main():
    # load the dataframe of route popularity
    pairs = pd.read_csv("../data/processed/connections_csv.csv")
    # load the stations
    stations = pd.read_csv("../data/processed/stationLookup.csv", index_col="short_name")
    lookup_series = stations.loc[:,['lat','lon']]

    # %%

    # combine the stations and the route popularity, and make them into tuples of the latlongs
    mergedf = (
        pairs.merge(
            lookup_series, how="left", left_on="st", right_index=True, validate="m:1",
        )
        .rename(columns={"lon": "start_long","lat": "start_lat"})
        .merge(lookup_series, how="left", left_on="en", right_index=True, validate="m:1")
        .rename(columns={"lon": "end_long","lat": "end_lat"})
    )

    # %%
    # to limit the amount of memory, we do the database loading in chunks
    for chunk in tqdm(array_split(mergedf, 100)):
        geomlist = [
            get_route(startx, starty, endx, endy)
            for starty,startx, endy,endx in chunk.iloc[:,3:].values
        ]
        # load the chunk into a gdf and write to the postgis database
        gpd.GeoDataFrame(chunk).assign(geom=geomlist).dropna().set_geometry('geom',crs="EPSG:4326").to_postgis(
            "station_routes", con=engine, if_exists="append", index=False
        )

if __name__ == '__main__':
    main()
