# %%
import numpy as np
import pandas as pd
from numpy.lib.recfunctions import append_fields

# %%

filelist = ['D:/Projects/cabi-data/data/tripdata/202004-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202005-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202006-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202007-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202008-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202009-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202010-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202011-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202012-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202101-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202102-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202103-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202104-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202105-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202106-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202107-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202108-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202109-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202110-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202111-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202112-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202201-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202202-capitalbikeshare-tripdata.csv',
'D:/Projects/cabi-data/data/tripdata/202203-capitalbikeshare-tripdata.csv']

cabi_dtype_newstyle = np.dtype(
    [
        ("ride_id", "U16"),
        ("rideable_type", "U13"),
        ("start_time", "datetime64[s]"),
        ("end_time", "datetime64[s]"),
        ("start_st_name", "U"),
        ("start_st_id", "<i4"),
        ("end_st_name", "U"),
        ("end_st_id", "<i4"),
        ("start_lat", "f"),
        ("start_lng", "f"),
        ("end_lat", "f"),
        ("end_lng", "f"),
        ("mem_cas", "U6"),
    ]
)


def new_load_rides_np(filename):
    ar = np.genfromtxt(
        filename,
        delimiter=",",
        dtype=cabi_dtype_newstyle,
        skip_header=1,
        usecols=(0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12),
    )
    return ar

# make a list of strcutred arrays and combine them together
# arraylist = [new_load_rides_np(filename) for filename in filelist]
# ar = np.hstack(arraylist)


# %%
full_array = new_load_rides_np(filelist[-1])

# drop self trips
ar = full_array[full_array['start_st_id']!=full_array['end_st_id']]

# drop 0 stations
ar = ar[ar['start_st_id']!=0]
ar = ar[ar['end_st_id']!=0]

# drop NA values
ar = ar[ar['start_st_id']!=-1]
ar = ar[ar['end_st_id']!=-1]

startids = ar['start_st_id']
endids = ar['end_st_id']


combos,counts = np.unique(ar[['start_st_id','end_st_id']],return_counts=True)

poparray = append_fields(combos, 'pop', counts,usemask=False)

# %%
