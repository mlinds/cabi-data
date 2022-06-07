from os import listdir
from multiprocessing import Pool

import geopandas as gpd
import numpy as np
import pandas as pd

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


def _load_files(filenames: list):
    # two different styles, old and new

    for filename in filenames:
        columns = pd.read_csv(filename, nrows=2).columns
        # determine if the csv is the old or new format

        if columns[0] == "Duration":
            yield _load_old_style(filename)
        elif columns[0] == "ride_id":
            yield _load_new_style(filename)


def return_trip_datatable(datafolder="../data/tripdata/"):
    """
    Reads CSV files and returns a DataFrame of the trips.

    Parameters:
    datafolder: pathlike: location of the CSVs of all the cabi trips you are interested in
    """

    data_files = [datafolder + filename for filename in listdir(datafolder)]
    df = pd.concat(_load_files(data_files))
    df["member_casual"] = df["member_casual"].str.lower()
    df["member_casual"] = df["member_casual"].astype("category")
    return df

def _get_station_dataframe():
    """
    Queries the public cabi GBFS api and returns a DataFrame of the stations
    """
    # get a raw dataframe of the current status of the system
    df = pd.read_csv("../data/processed/stationLookup.csv")
    stations = df.assign(short_name=df.short_name.astype("uint32"))
    return stations


_stations = _get_station_dataframe()


def _get_station_GeoDF():
    geometry = [Point(xy) for xy in zip(_stations.lon, _stations.lat)]
    return gpd.GeoDataFrame(_stations, crs="EPSG:4326", geometry=geometry)


def find_station_geo(stationnum: int):
    """
    Accepts a station ID and returns a tuple of the latitude and longitude in WGS84
    """
    matched = _stations[_stations.short_name == stationnum]
    try:
        latval = float(matched.lat.values)
        lonval = float(matched.lon.values)
        return (lonval, latval)
    except:
        return None


def make_trip_geometry(start_station_num: int, end_station_num: int):
    """
    Takes 2 stations and returns a linestring between them.


    """
    start_point = find_station_geo(start_station_num)
    end_point = find_station_geo(end_station_num)
    try:
        return LineString((start_point, end_point))
    except:
        return pd.NA

_stations_state_plane = (
    _get_station_GeoDF().to_crs(epsg=26985).set_index("short_name").geometry
)

def saves_to_parquet(path, df):
    df = return_trip_datatable()
    df.to_parquet(path, compression="gzip")


def read_stored_trips(path="../data/interim/comb_trips.gzip"):
    return pd.read_parquet(path)
