#%%
from cabi import return_trip_datatable
from sqlalchemy import create_engine
from tqdm import tqdm

# %%

df = return_trip_datatable(r"../tripdata/")
# %%
# to ensure that this slow process doesn't get hung up
# we are going to load in chunks and use the tqdm module to
# create a status bar

# create the chunks
n = 200000  # chunk row size
list_df = [df[i : i + n] for i in tqdm(range(0, df.shape[0], n))]

# create SQL alchemy database connection
engine = create_engine("postgresql://postgres:password@127.0.0.1:5432/postgres")

for chunk in tqdm(list_df):
    chunk.to_sql(
        "trips",
        engine,
        if_exists="append",
    )

# %%

# put the stations in the database
# stations = load_stations()
# stations.to_postgis("stations", engine)

#%%
