#%%

import pydeck as pdk
import pandas as pd

# %%


cabi_stations = "https://raw.githubusercontent.com/mlinds/cabi-data/main/data/processed/stationLookup.csv"
connections_path = "https://raw.githubusercontent.com/mlinds/cabi-data/main/data/processed/connections_csv.csv"

trips = pd.read_csv(connections_path)
stations = pd.read_csv(cabi_stations)
df = trips.merge(stations,left_on='st',right_on='short_name',).merge(stations,left_on='en',right_on='short_name',suffixes=('_st','_en'),)

# Filter to the most popular 10%
df = df[df.popularity > df.popularity.quantile(.95)]

# %%
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]


# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="S000 * 2",
    get_source_position=["lon_st", "lat_st"],
    get_target_position=["lon_en", "lat_en"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=38.896670, longitude=-77.028874, bearing=45, pitch=50, zoom=8,)


TOOLTIP_TEXT = {"html": "{S000} jobs <br /> Home of commuter in red; work location in green"}
r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
r.to_html("../reports/arc_layer.html")
# %%
