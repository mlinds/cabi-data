from os import listdir

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.core.dtypes import dtypes
from shapely.geometry import LineString, Point


def _load_files(filenames: list):
    chunksize = 1000
    # two different styles, old and new
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

    ride_dtypes = {
        "started_at": "str",
        "ended_at": "str",
        "start_station_id": "Int64",
        "end_station_id": "Int64",
        "member_casual": pd.CategoricalDtype(
            ["Member", "Casual", "member", "casual", "Unknown"]
        ),
    }

    for filename in filenames:
        columns = pd.read_csv(filename, nrows=2).columns
        # determine which type of file we are reading
        # TODO change to match statement
        if columns[0] == "Duration":
            try:
                yield pd.read_csv(
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
        elif columns[0] == "ride_id":
            try:
                yield pd.read_csv(
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


def return_trip_datatable(datafolder="tripdata/"):
    """
    Returns a pandas DataFrame of all CaBi trips if you tell it where you keep your trip CSVss
    """

    data_files = [datafolder + filename for filename in listdir(datafolder)]
    return pd.concat(_load_files(data_files))


# return_trip_datatable()


def read_and_save_trips():
    """
    Saves all the trips to a hdf5 file
    """
    data = return_trip_datatable()
    data.to_hdf("outputs/trips.h5", key="trips", mode="w", format="fixed", complevel=5)
    return None


def load_stations():
    df = pd.read_json(
        "https://gbfs.capitalbikeshare.com/gbfs/en/station_information.json"
    )
    datalist = df.iloc[0, 0]
    df = pd.DataFrame(datalist)
    # df.rename({"short_name": "NAME"}, inplace=True)
    stations = df.assign(short_name=df.short_name.astype("int"))
    geometry = [Point(xy) for xy in zip(stations.lat, stations.lon)]
    return gpd.GeoDataFrame(stations, crs="EPSG:4326", geometry=geometry)


a = pd.DataFrame(load_stations())


def find_station_geo(stationnum):
    matched = a[a.short_name == stationnum]
    try:
        latval = matched.lat
        lonval = matched.lon
        return (lonval, latval)
    except:
        return None


def make_trip_geometry(start_station_num: int, end_station_num: int):
    """ """
    start_point = find_station_geo(start_station_num)
    end_point = find_station_geo(end_station_num)
    try:
        return LineString((start_point, end_point))
    except:
        return pd.NA


def pair_stations(start_ids, end_ids):
    l = []
    for x, y in zip(start_ids, end_ids):
        xs, ys = sorted([int(x), int(y)])
        l.append(int(str(xs) + str(ys)))
    return l

def get_dist(start_id, end_id):
    geom = make_trip_geometry(start_id, end_id)
    