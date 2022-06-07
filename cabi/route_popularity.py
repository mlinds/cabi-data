# %%
import cabi
import pandas as pd

def calculate_popularity():
    df = pd.read_parquet("../data/interim/comb_trips.gzip")
    total = len(df)
    print(f'{total:,} CaBi trips were found up to {df.ended_at.max()}')
    # get the raw value counts
    vc = df[['start_station_id','end_station_id']].value_counts().reset_index().rename(columns={0:'popularity'})
    print(f'{len(vc):,} unique pairs found')
    
    # drop selftrips
    vc = vc[~(vc.start_station_id==vc.end_station_id)]
    print(f'{len(vc):,} unique pairs after removing trips starting and ending at same dock')
    # drop trips with zero
    vc = vc[~(vc.start_station_id==0)]
    vc = vc[~(vc.end_station_id==0)]
    print(f'{len(vc):,} unique pairs after removing invalid trips')
    # create a new dataframe that combines trips from A to B with trips from B to A
    sorted_df = vc.apply(lambda x:sorted([x.start_station_id,x.end_station_id]),axis=1,result_type='expand')
    # horizontal stack the sorted one
    # group by the sorted stations, drop the columns we no longer need,rename the columns we do want then sort on numeric values 
    comb_df = pd.concat([vc,sorted_df],axis=1).groupby([0,1]).sum().reset_index().drop(columns=['start_station_id','end_station_id']).rename(columns={0:'st',1:'en'}).sort_values(by=['st','en'],ascending=[True,True],ignore_index=True)
    print(f'{len(comb_df):,} trip pairs after summing')
    return comb_df 
    
def update_popularity(update_csv=True,update_postgis=True):
    if not update_csv and not update_postgis:
        raise ValueError('need at least one')
    print('Calculating route popularity')
    pop_df = calculate_popularity()
    if update_csv:
        pop_df.to_csv(
            "../data/processed/connections_csv.csv",
            columns=["st", "en", "popularity"],
            index=False,
        )
        print('results written to CSV file')
    if update_postgis:
        from sqlalchemy import create_engine
        engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/cabidb")
        pop_df.to_sql(name='station_popularity',con=engine,if_exists='replace')
        print('Station popularity written to PostGIS table')
        
if __name__ == '__main__':
    update_popularity()
