# %% 
import pandas as pd
import geopandas as gpd
import cabi 

df_pop = pd.read_csv('../data/processed/connections_csv.csv')
station_df = cabi._get_station_GeoDF().to_crs(crs='EPSG:26985')

station_df = station_df.assign(x=station_df.geometry.x,y=station_df.geometry.y)

stat_lat = station_df.set_index('short_name').y
stat_lon = station_df.set_index('short_name').x
cluster_gdf = gpd.read_file('../data/interim/clustered_edges.gpkg')

df_startcoords = df_pop.merge(stat_lat,left_on='st',right_index=True
).rename(columns={'y':'y_start'}
).merge(stat_lon,left_on='st',right_index=True).rename(columns={'x':'x_start'}
).merge(stat_lat,left_on='en',right_index=True).rename(columns={'y':'y_end'}
).merge(stat_lon,left_on='en',right_index=True).rename(columns={'x':'x_end'}
).merge(cluster_gdf,left_on=['st','en'],right_on=['st','en'])

# df_startcoords[(df_startcoords.st.isin(stationlist)) | (df_startcoords.en.isin(stationlist))].to_csv(r'D:\Projects\fdeb-fortran\fdeb\test_bundling_edges.csv',index=False)
def make_csv_by_cluster(cluster_num):
# df_startcoords = df_startcoords[(df_pop.st.isin(stationlist)) | (df_pop.en.isin(stationlist))]
    df_startcoords[df_startcoords.CLUSTER_ID==cluster_num].to_csv(rf'D:\Projects\fdeb-fortran\fdeb\clusters\cluster{cluster_num}_edges.csv',index=False)
# df_pop.merge(station_df,right_on='short_name',left_on='st',suffixes=(None,'_start' )).merge(station_df,right_on='short_name',left_on='st',suffixes=(None,'_end')).to_csv('../data/interim/test_bundling_edges.csv',index=False,columns=['st','en','popularity','x','y','x_end','y_end'])
# %%
for clusternum in range(1,30):
    make_csv_by_cluster(clusternum)
# %%
