# %%
import cabi
import pandas as pd
import numpy as np
# %% [markdown]
# # Finding CaBi Stations that no longer exist

# in the dataset of all CaBi trips, there are a number that refer to stations that no longer exist in the table of CaBi stations. All the trip csvs include the station names, so this can be used to find the location of these

# %%
# we drop anything with an NA value
df = pd.read_parquet("../data/interim/comb_trips.gzip").dropna()

# %%
start_station_array = df.start_station_id.unique()
end_station_array = df.end_station_id.unique()
all_stations = np.unique(np.hstack([start_station_array,end_station_array]))
# %%
def get_station_dataframe():
    """
    Queries the public cabi GBFS api and returns a DataFrame of the stations
    """
    df = pd.read_json(
        "https://gbfs.capitalbikeshare.com/gbfs/en/station_information.json"
    )
    df = pd.DataFrame(df.iloc[0, 0])
    stations = df.assign(short_name=df.short_name.astype("uint32"),legacy_id=df.legacy_id.astype('int'))

    return stations
stations_current = get_station_dataframe()
# %%
stations_cabi = pd.read_csv('../data/processed/stationLookup.csv')

# %%
missing_stations = all_stations[~pd.Series(all_stations).isin(stations_cabi.short_name)]

# %%
final_stations.to_csv('../data/processed/stationLookup.csv',index=False)
# %%
