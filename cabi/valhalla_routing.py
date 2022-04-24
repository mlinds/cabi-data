# %%
import requests
import geopandas as gpd
from shapely.geometry import shape
import pandas as pd
from numpy import array_split
from itertools import islice
from sqlalchemy import create_engine
from tqdm import tqdm
import json
from shapely.geometry import LineString
import numpy as np
from valhalla import Actor, get_config, get_help

engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/pgrouting_data")
#%%

#decode an encoded string
def decode(encoded):
    #six degrees of precision in valhalla
  inv = 1.0 / 1e6;
  decoded = []
  previous = [0,0]
  i = 0
  #for each byte
  while i < len(encoded):
    #for each coord (lat, lon)
    ll = [0,0]
    for j in [0, 1]:
      shift = 0
      byte = 0x20
      #keep decoding bytes until you have this coord
      while byte >= 0x20:
        byte = ord(encoded[i]) - 63
        i += 1
        ll[j] |= (byte & 0x1f) << shift
        shift += 5
      #get the final value adding the previous offset and remember it for the next
      ll[j] = previous[j] + (~(ll[j] >> 1) if ll[j] & 1 else (ll[j] >> 1))
      previous[j] = ll[j]
    #scale by the precision and chop off long coords also flip the positions so
    #its the far more standard lon,lat instead of lat,lon
    decoded.append([float('%.6f' % (ll[1] * inv)), float('%.6f' % (ll[0] * inv))])
  #hand back the list of coordinates
  return decoded

# tool that queries the running instance of OSMR
def get_route(startx, starty, endx, endy):
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

    r = requests.get(f"http://127.0.0.1:8002/route?json=" + json.dumps(requeststring))
    if r.status_code == 400:
        return np.NaN
    polyline_enc = r.json()['trip']['legs'][0]['shape']
    polyline_dec = decode(polyline_enc)

    return LineString(polyline_dec)

# %%
# load the dataframe of route popularity
pairs = pd.read_csv("../data/processed/connections_csv.csv")
# load the stations
stations = pd.read_csv("../data/processed/stationLookup.csv", index_col="short_name")
lookup_series = pd.Series(
    list(stations.loc[:, ["lon", "lat"]].itertuples(index=False, name=None)),
    index=stations.index,
    name="latlong",
)

# combine the stations and the route popularity, and make them into tuples of the latlongs
mergedf = (
    pairs.merge(
        lookup_series, how="left", left_on="st", right_index=True, validate="m:1"
    )
    .rename(columns={"latlong": "start_latlong"})
    .merge(lookup_series, how="left", left_on="en", right_index=True, validate="m:1")
    .rename(columns={"latlong": "end_latlong"})
)

# %%
# to limit the amount of memory, we do the database loading in chunks
for chunk in tqdm(array_split(mergedf, 100)):
    geomlist = [
        get_route(*startlatlong, *endlatlong)
        for startlatlong, endlatlong in zip(chunk.start_latlong, chunk.end_latlong)
    ]
    gpd.GeoDataFrame(chunk).assign(geom=geomlist).dropna().set_geometry('geom',crs="EPSG:4326").to_postgis(
        "station_routes", con=engine, if_exists="append", index=False
    )

# %%
