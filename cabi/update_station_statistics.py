# %%
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


# calculate the new statistics and check for new cabi stations

# first, get the dataframe of all trips, and the current info on the stations


def find_unique_stations(trips_df):
    trips_df = trips_df.dropna()
    start_station_array = trips_df.start_station_id.unique()
    end_station_array = trips_df.end_station_id.unique()
    return np.unique(np.hstack([start_station_array, end_station_array]))


def get_popularity(trips_df):
    starts = (
        trips_df[["start_station_id", "end_station_id"]]
        .groupby("start_station_id")
        .count()
        .reset_index()
        .rename(columns={"start_station_id": "station", "end_station_id": "tripcount"})
    )
    ends = (
        trips_df[["start_station_id", "end_station_id"]]
        .groupby("end_station_id")
        .count()
        .reset_index()
        .rename(columns={"end_station_id": "station", "start_station_id": "tripcount"})
    )

    tripscount = pd.concat([starts, ends]).groupby("station").sum().reset_index()

    self_trips = trips_df[trips_df.start_station_id == trips_df.end_station_id]
    round_trips_count = (
        self_trips.groupby("start_station_id")
        .count()
        .reset_index()
        .loc[:, ["start_station_id", "started_at"]]
        .rename(columns={"start_station_id": "station", "started_at": "roundtrips"})
    )

    count_by_station = (
        tripscount.merge(round_trips_count, how="left")
        .convert_dtypes()
        .set_index("station")
    )
    count_by_station = count_by_station[count_by_station.index != 0]
    return count_by_station


def update_stations_stat_table():
    trips_df = pd.read_parquet("../data/interim/comb_trips.gzip")
    current_station_data = pd.read_csv(
        "../data/processed/stationLookup.csv", usecols=[0, 1, 2, 3]
    )
    # check that there are not any trips to stations we don't know about
    all_unique_stations = find_unique_stations(trips_df)

    # TODO find a way to see if there are any trips here that aren't in station data table
    popularity = get_popularity(trips_df)
    merged_df = current_station_data.merge(
        popularity, how="left", left_on="short_name", right_on="station", validate="1:1"
    )

    return merged_df.loc[:, ["short_name", "tripcount", "roundtrips"]]


def write_stats():
    df = update_stations_stat_table()
    df.to_csv("../data/processed/station_stats.csv", index=False)
    print("Stats per station written to CSV file")

    engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/cabidb")
    df.to_sql(name="station_stats", con=engine, if_exists="replace")
    print("Stats written to SQL database")


# %%
if __name__ == "__main__":
    write_stats()
