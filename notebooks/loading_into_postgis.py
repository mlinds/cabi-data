#%%

from sqlalchemy import create_engine

from numpy_experiments import new_load_rides_np,filelist
import pandas as pd
import osmnx as onx

# %%

# setup a test array


ar = new_load_rides_np(filelist[-1])


df = pd.DataFrame(ar)


# create SQL alchemy database connection

engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/pgrouting_data")

# %%

df.to_sql(

    "trips",
    engine,

    if_exists="fail",
)

# %%
cabi_stations = "https://raw.githubusercontent.com/mlinds/cabi-data/main/data/processed/stationLookup.csv"

station_df = pd.read_csv(cabi_stations)

station_df.to_sql('cabi_stations',engine,index=False)
