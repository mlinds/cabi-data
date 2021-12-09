import cabi

def test_load_stations():
    station_df = cabi.load_stations()
    print(station_df.columns)


def test_find_station_geo():
    station = 31000
    lat,lon = cabi.find_station_geo(station)
    assert lat == 38.858971
    assert lon == -77.053230