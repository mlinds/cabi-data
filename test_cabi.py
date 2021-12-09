import cabi
import pandas as pd 
import numpy as np


def test_load_stations():
    station_df = cabi.load_stations()
    assert station_df.short_name.dtype is np.dtype('int32')


def test_find_station_geo():
    station = 31000
    print(station)
    lat,lon = cabi.find_station_geo(station)
    assert float(lon) == 38.858971
    assert float(lat) == -77.053230

def test_get_dist():
    distance = cabi.get_dist(31000,31003)
