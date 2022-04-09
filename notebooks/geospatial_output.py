#%%
from cabi import return_trip_datatable
import cabi
from geopandas import GeoDataFrame

#%%
df = return_trip_datatable()
directed = pd.DataFrame(
    df[["start_station_id", "end_station_id"]].value_counts()
).reset_index()

# %%
# set up geometry
geo = [
    cabi.make_trip_geometry(st, end)
    for st, end in zip(directed.start_station_id, directed.end_station_id)
]


# %%

gdf = GeoDataFrame(directed, geometry=geo, crs="EPSG:4326")

# %%
gdf.convert_dtypes().to_file("../data/interim/geo_edges.gpkg", driver="GPKG")

# %%
gdf.dtypes
# %%
