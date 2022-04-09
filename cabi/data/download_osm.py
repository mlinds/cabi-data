import osmnx
from cabi import _get_station_dataframe


def save_OSM_graph(filepath):
    """
    Downloads the OSM data for the bounding box of the current station and saves it to filepath specified

    filepath: os.pathlike: Location to save the OSM XML data
    """
    df = _get_station_dataframe()
    bbox = [df.lat.max(), df.lat.min(), df.lon.min(), df.lon.max()]
    G = osmnx.graph_from_bbox(*bbox, network_type="bike")
    osmnx.save_graph_xml(G, filepath=filepath)

    return None