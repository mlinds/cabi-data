from os import listdir
from multiprocessing import Pool

import geopandas as gpd
import numpy as np
import pandas as pd

from tqdm import tqdm
from shapely.geometry import LineString, Point

ride_dtypes = {
    "started_at": "str",
    "ended_at": "str",
    "start_station_id": "UInt16",
    "end_station_id": "UInt16",
    "member_casual": pd.CategoricalDtype(
        ["Member", "Casual", "member", "casual", "Unknown"]
    ),
}


def _load_old_style(filename):
    old_cols = [
        "Duration",
        "started_at",
        "ended_at",
        "start_station_id",
        "start_station_name",
        "end_station_id",
        "end_station_name",
        "Bike number",
        "member_casual",
    ]

    try:
        return pd.read_csv(
            filename,
            parse_dates=["started_at", "ended_at"],
            usecols=[1, 2, 3, 5, 8],
            header=0,
            names=old_cols,
            dtype=ride_dtypes,
            engine="c",
            infer_datetime_format=True,
        )
    except:
        raise TypeError(f"Error encountered at {filename}")


def _load_new_style(filename):
    new_cols = [
        "ride_id",
        "rideable_type",
        "started_at",
        "ended_at",
        "start_station_name",
        "start_station_id",
        "end_station_name",
        "end_station_id",
        "start_lat",
        "start_lng",
        "end_lat",
        "end_lng",
        "member_casual",
    ]

    try:
        return pd.read_csv(
            filename,
            header=0,
            parse_dates=["started_at", "ended_at"],
            usecols=[2, 3, 5, 7, 12],
            names=new_cols,
            dtype=ride_dtypes,
            engine="c",
            infer_datetime_format=True,
        )
    except:
        # with so many files it helps to know which is causing issues
        raise TypeError(
            f"Error encountered at {filename} - columns do not match expected pattern"
        )


def _load_file(filename: str):
    # two different styles, old and new

    # for filename in filenames:
    columns = pd.read_csv(filename, nrows=2).columns
    # determine if the csv is the old or new format

    if columns[0] == "Duration":
        return _load_old_style(filename)
    elif columns[0] == "ride_id":
        return _load_new_style(filename)


def return_trip_datatable(datafolder="../data/tripdata/"):
    """
    Reads CSV files and returns a DataFrame of the trips.

    Parameters:
    datafolder: pathlike: location of the CSVs of all the cabi trips you are interested in
    """

    data_files = [datafolder + filename for filename in listdir(datafolder)]
    dflist = [_load_file(pathname) for pathname in tqdm(data_files)]

    df = pd.concat(dflist)
    # clean up names
    df["member_casual"] = df["member_casual"].str.lower()
    df["member_casual"] = df["member_casual"].astype("category")
    return
