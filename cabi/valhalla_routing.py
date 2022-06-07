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

import sys
import warnings

sys.warnoptions='ignore'
engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/cabidb")
warnings.simplefilter('ignore')
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
        # return response
        polyline_enc = response['trip']['legs'][0]['shape']
        polyline_dec = decode_polyline(polyline_enc)
        time = response['trip']['legs'][0]['summary']['time']
        length = response['trip']['legs'][0]['summary']['length']
        return LineString(polyline_dec),time,length
    except RuntimeError:
        print(f'{(startx, starty, endx, endy)} could not be routed')
        return np.NaN,np.NaN,np.NaN
# %%
def main():
    # load the dataframe of route popularity
    pairs = pd.read_csv("../data/processed/connections_csv.csv")
    # load the stations
    stations = pd.read_csv("../data/processed/stationLookup.csv", index_col="short_name")
    # get a list of the stations we already have in the PostGIS db
    existing_routes_df = pd.read_sql_query('select st,en from station_routes', engine)
    station_combo_list = (existing_routes_df.st.astype('str')+existing_routes_df.en.astype('str')).astype('int64')
    # datframe of lat and long indexed by the station id
    lookup_series = stations.loc[:,['lat','lon']]

    # we find new unique pairs not already in the database
    new_pairs = pairs[~(pairs.st.astype('str') + pairs.en.astype('str')).astype('int64').isin( list(station_combo_list))]    
    
    if len(new_pairs) == 0:
        print('No new station combos were found')
        return
    print(len(new_pairs),"New station combinations were found in the data.")
    # combine the stations and the route popularity, and make them into tuples of the latlongs
    mergedf = (
        new_pairs.merge(
            lookup_series, how="left", left_on="st", right_index=True, validate="m:1",
        )
        .rename(columns={"lon": "start_long","lat": "start_lat"})
        .merge(lookup_series, how="left", left_on="en", right_index=True, validate="m:1")
        .rename(columns={"lon": "end_long","lat": "end_lat"})
    )


# %%
    for chunk in tqdm(array_split(mergedf, 200)):
        geomlist=[]
        timelist = []
        distlist = []
        for starty,startx, endy,endx in chunk.iloc[:,3:].values:   
            geometry,time,distance = get_route(startx, starty, endx, endy)
            geomlist.append(geometry)
            timelist.append(time)
            distlist.append(distance)
        # load the chunk into a gdf and write to the postgis database
        gpd.GeoDataFrame(chunk).assign(geom=geomlist,triptime=timelist,tripdist=distlist).dropna().set_geometry('geom',crs="EPSG:4326").to_crs('EPSG:26985').to_postgis(
            "station_routes", con=engine, if_exists="append", index=False
        )
#%%
if __name__ == '__main__':
    main()

# %%
