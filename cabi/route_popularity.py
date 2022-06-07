# %%
import cabi
import pandas as pd
from sqlalchemy import create_engine


# %%
df = pd.read_parquet("../data/interim/comb_trips.gzip")
total = len(df)
print(f"{total} total trips")

# %%
vc = df[['start_station_id','end_station_id']].value_counts().reset_index().rename(columns={0:'popularity'})
vc = vc[~(vc.start_station_id==vc.end_station_id)]
vc = vc[~(vc.start_station_id==0)]
vc = vc[~(vc.end_station_id==0)]
sorted_df = vc.apply(lambda x:sorted([x.start_station_id,x.end_station_id]),axis=1,result_type='expand')
comb_df = pd.concat([vc,sorted_df],axis=1)

pop_df = comb_df.groupby([0,1]).sum().reset_index().drop(columns=['start_station_id','end_station_id']).rename(columns={0:'st',1:'en'}).sort_values(by=['st','en'],ascending=[True,True],ignore_index=True)

# %%
pop_df.to_csv(
    "../data/processed/connections_csv.csv",
    columns=["st", "en", "popularity"],
    index=False,
)

#%%
engine = create_engine("postgresql://admin:maxpass@127.0.0.1:5432/cabidb")

#%%
pop_df.to_sql(name='station_popularity',con=engine,if_exists='replace')

# %%


