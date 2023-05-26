import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine

def main():
    """ load the csv file containing the stations, get the geometry of the locations, and load it into the postgis database
    """    
    # establish the database connection
    engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/cabidb")
    # load the dataframe of cabi stations=
    cabi_stations = pd.read_csv('./data/processed/stationLookup.csv',index_col=0)
    # create a geopandas geometry object
    point_geom = gpd.points_from_xy(x=cabi_stations.lon,y=cabi_stations.lat,crs='EPSG:4326')
    # create a geodataframe
    cabi_stations_geo = gpd.GeoDataFrame(cabi_stations,geometry=point_geom)
    # add the table the to the postgis database
    cabi_stations_geo.to_postgis('cabi_stations', engine,if_exists='replace')

if __name__ == '__main__':
    main()