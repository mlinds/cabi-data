from operator import ge

import cabi
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import LineString
import pytest
from cabi.testdata import testdata_trips


def test_load_stations():
    station_df = cabi._get_station_dataframe()
    assert station_df.short_name.dtype is np.dtype("uint32")
    assert type(station_df) is pd.DataFrame
    station_df = cabi._get_station_dataframe()


def test_find_station_geo():
    station = 31000
    lat, lon = cabi.find_station_geo(station)
    assert float(lon) == 38.858971
    assert float(lat) == -77.053230


def test_get_dist():
    distance = cabi.get_dist(31000, 31003)
    assert type(distance) is float

    with pytest.raises(KeyError):
        cabi.get_dist(50, 31003)

    with pytest.raises(KeyError):
        cabi.get_dist(31003, "as")


def test_make_trip_geometry():
    geometry = cabi.make_trip_geometry(31000, 31003)
    assert type(geometry) is LineString


def test_get_triptime():
    testdf = pd.DataFrame(testdata_trips)
    time = cabi.get_triptime(testdf.started_at, testdf.ended_at)
    # assert time.dtype is pd.Timedelta
