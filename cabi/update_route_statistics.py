import pandas as pd
import numpy as np

# TODO at time statistics from stats.ipynb
# TODO after refining these functions, write one single script with an if__name... block that imports and calls the other functions


def calculate_time_statistics(tripdata):
    print("Starting calculation of time statistics")
    # remove trips with 0 for start or end
    tripdata = tripdata.loc[
        (tripdata.end_station_id != 0) & (tripdata.start_station_id != 0)
        # recalculate to consider time zones and just drop times we don't know
    ]
    tripdata=tripdata.assign(started_at=tripdata.started_at.dt.tz_localize('America/New_York',ambiguous='NaT'),ended_at=tripdata.ended_at.dt.tz_localize('America/New_York',ambiguous='NaT'))
    # add time in minutes
    triptimedf = tripdata.assign(
        triptime=(tripdata.ended_at - tripdata.started_at).dt.total_seconds() / 60
    )
    # calculate summary stats
    time_summary = (
        triptimedf.loc[:, ["start_station_id", "end_station_id", "triptime"]]
        .groupby(["start_station_id", "end_station_id"])
        .agg(
            {"triptime": [np.mean, np.median, np.std, np.min, np.max, np.count_nonzero]}
        )
        .loc[:, "triptime"]
        .reset_index()
        .round(4)
        # assign more readable names to column
        .rename(
            columns={
                "start_station_id": "st",
                "end_station_id": "en",
                "count_nonzero": "TripCount",
                "mean": "meanTime_min",
                "median": "medianTime_min",
                "std": "timeStddev_min",
                "amin": "timeMin_min",
                "amax": "timeMax_min",
            }
        )
    )
    return time_summary


def update_time_stats(procssed_time_stats, update_csv=True, update_postgis=True):
    if not update_csv and not update_postgis:
        raise ValueError("need at least one")

    if update_csv:
        procssed_time_stats.to_csv(
            "../data/processed/bidirectional_stats.csv",
            # columns=["st", "en", "popularity"],
            index=False,
        )
        print("Time statistics written to CSV file")
    if update_postgis:
        from sqlalchemy import create_engine

        engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/cabidb")
        procssed_time_stats.to_sql(
            name="route_time_statistics", con=engine, if_exists="replace"
        )
        print("Time statistics written to PostGIS table")


def calculate_popularity(df):
    print("Calculating route popularity statistics")
    total = len(df)
    print(f"{total:,} CaBi trips were found up to {df.ended_at.max()}")
    # get the raw value counts
    vc = (
        df[["start_station_id", "end_station_id"]]
        .value_counts()
        .reset_index()
        .rename(columns={0: "popularity"})
    )
    print(f"{len(vc):,} unique pairs found")

    # drop selftrips
    vc = vc[~(vc.start_station_id == vc.end_station_id)]
    print(
        f"{len(vc):,} unique pairs after removing trips starting and ending at same dock"
    )
    # drop trips with zero
    vc = vc[~(vc.start_station_id == 0)]
    vc = vc[~(vc.end_station_id == 0)]
    print(f"{len(vc):,} unique pairs after removing invalid trips")
    # create a new dataframe that combines trips from A to B with trips from B to A
    sorted_df = vc.apply(
        lambda x: sorted([x.start_station_id, x.end_station_id]),
        axis=1,
        result_type="expand",
    )
    # horizontal stack the sorted one
    # group by the sorted stations, drop the columns we no longer need,rename the columns we do want then sort on numeric values
    comb_df = (
        pd.concat([vc, sorted_df], axis=1)
        .groupby([0, 1])
        .sum()
        .reset_index()
        .drop(columns=["start_station_id", "end_station_id"])
        .rename(columns={0: "st", 1: "en"})
        .sort_values(by=["st", "en"], ascending=[True, True], ignore_index=True)
    )
    print(f"{len(comb_df):,} trip pairs after summing")
    return comb_df


def update_popularity(pop_df, update_csv=True, update_postgis=True):
    if not update_csv and not update_postgis:
        raise ValueError("need at least one")
    print("Calculating route popularity")
    # pop_df = calculate_popularity()
    if update_csv:
        pop_df.to_csv(
            "../data/processed/route_stats.csv",
            columns=["st", "en", "popularity"],
            index=False,
        )
        print("results written to CSV file")
    if update_postgis:
        from sqlalchemy import create_engine

        engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/cabidb")
        pop_df.to_sql(name="route_stats", con=engine, if_exists="replace")
        print("Station popularity written to PostGIS table")


def main():
    alltrips = pd.read_parquet("../data/interim/comb_trips.gzip")
    timedf = calculate_time_statistics(alltrips)
    update_time_stats(timedf)
    pop_df = calculate_popularity(alltrips)
    update_popularity(pop_df)


if __name__ == "__main__":
    main()
