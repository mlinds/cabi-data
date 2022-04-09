#%%

import pydeck as pdk
import pandas as pd
from numpy import log10

# %%

cabi_stations = "https://raw.githubusercontent.com/mlinds/cabi-data/main/data/processed/stationLookup.csv"

df = pd.read_parquet("../data/interim/comb_trips.gzip")
stations = pd.read_csv(cabi_stations)
df = df[df.started_at.between("2022-03", "2022-4")].dropna()

df = (
    df.groupby(by=["start_station_id", "end_station_id"])
    .count()
    .reset_index()[["start_station_id", "end_station_id", "started_at"]]
)
df.rename(columns={"started_at": "popularity"}, inplace=True)
df = df.merge(stations, left_on="start_station_id", right_on="short_name",).merge(
    stations,
    left_on="end_station_id",
    right_on="short_name",
    suffixes=("_st", "_en"),
)

df = df[df.popularity > df.popularity.quantile(0.9)]
# %%
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]


# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="popularity/10",
    get_source_position=["lon_st", "lat_st"],
    get_target_position=["lon_en", "lat_en"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=38.896670,
    longitude=-77.028874,
    bearing=0,
    pitch=50,
    zoom=10,
)


TOOLTIP_TEXT = {"html": "{popularity} Trips in March 2022"}
r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
r.to_html("../reports/march_arcs.html")
# %%
