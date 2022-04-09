import pandas as pd
from cabi.cabi import _get_station_dataframe

if __name__ == "__main__":
    df = _get_station_dataframe()
    datalist = df.iloc[0, 0]
    df = pd.DataFrame(datalist)

    df[["short_name", "name"]].to_json(
        "../data/interim/stations.json", orient="table", index=False
    )
