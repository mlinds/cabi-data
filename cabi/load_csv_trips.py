# %%
from tripio import return_trip_datatable


def update_parquet():
    parquetpath = "../data/interim/comb_trips.gzip"
    tripdf = return_trip_datatable()
    tripdf.to_parquet(parquetpath, compression="gzip")
    print(f"{len(tripdf):,} trips were written to Parquet file {parquetpath}")


"../data/processed/stationLookup.csv"
#%%

#%%
if __name__ == "__main__":
    update_parquet()
