#%%
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import json

# %%
nodes = pd.read_csv("../data/stationLookup.csv", usecols=["short_name", "name"])

edges = pd.read_json("../data/all_trips.json", orient="split").sort_values(
    "popularity", ascending=False
)


# %%
# create iterables that are easily fed into networkx contstructors
nodelist = [(short_name) for short_name in nodes.short_name]
edgelist = [
    (start, end, popularity)
    for start, end, popularity in edges[edges.popularity > 10000].itertuples(
        index=False
    )
]
# %%
G = nx.MultiDiGraph()
G.add_nodes_from(nodelist)
G.add_weighted_edges_from(edgelist, weight="popularity")


# %%

json_dict = nx.node_link_data(G)
json_string = json.dumps(json_dict)

# %%
with open("../data/graph_json.json", "w") as gr_json_file:
    gr_json_file.write(json_string)
# %%
plt.figure(figsize=(30, 30))
cmap = plt.colormaps['magma']
nx.draw_circular(
    G,
    # with_labels=True,
    edge_cmap=cmap,
    node_size=5,
    # edge_vmin=10000.0,
    # edge_vmax=54033.0,
    # edge_color=edges.popularity.values,
)
# nx.draw_networkx()
# %%
nx.draw_random(G, node_size=4)
# %%

#%%
nx.draw_spectral(G, node_size=4)
