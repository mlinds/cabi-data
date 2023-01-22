
var styleJSON = {
    "version": 8,
    "name": "qgis2web export",
    "pitch": 0,
    "light": {
        "intensity": 0.2
    },
    "sources": {
        "DarkMatter_0": {
            "type": "raster",
            "tiles": ["http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"],
            "tileSize": 256
        },
        "cabi_network_stats_1": {
            "type": "geojson",
            "data": json_cabi_network_stats_1
        }
                    },
    "sprite": "",
    "glyphs": "https://glfonts.lukasmartinelli.ch/fonts/{fontstack}/{range}.pbf",
    "layers": [
        {
            "id": "background",
            "type": "background",
            "layout": {},
            "paint": {
                "background-color": "#ffffff"
            }
        },
        {
            "id": "lyr_DarkMatter_0_0",
            "type": "raster",
            "source": "DarkMatter_0"
        },
        {
            "id": "lyr_cabi_network_stats_1_0",
            "type": "line",
            "source": "cabi_network_stats_1",
            "layout": {},
            "paint": {'line-width': ['case', ['all', ['>=', ['get', 'popularity'], 1.0], ['<=', ['get', 'popularity'], 10.0]], 4.5, ['all', ['>', ['get', 'popularity'], 10.0], ['<=', ['get', 'popularity'], 100.0]], 4.5, ['all', ['>', ['get', 'popularity'], 100.0], ['<=', ['get', 'popularity'], 1000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 1000.0], ['<=', ['get', 'popularity'], 10000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 10000.0], ['<=', ['get', 'popularity'], 100000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 100000.0], ['<=', ['get', 'popularity'], 1000000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 1000000.0], ['<=', ['get', 'popularity'], 10000000.0]], 4.5, 0], 'line-opacity': ['case', ['all', ['>=', ['get', 'popularity'], 1.0], ['<=', ['get', 'popularity'], 10.0]], 1.0, ['all', ['>', ['get', 'popularity'], 10.0], ['<=', ['get', 'popularity'], 100.0]], 1.0, ['all', ['>', ['get', 'popularity'], 100.0], ['<=', ['get', 'popularity'], 1000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 1000.0], ['<=', ['get', 'popularity'], 10000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 10000.0], ['<=', ['get', 'popularity'], 100000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 100000.0], ['<=', ['get', 'popularity'], 1000000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 1000000.0], ['<=', ['get', 'popularity'], 10000000.0]], 1.0, 0], 'line-color': ['case', ['all', ['>=', ['get', 'popularity'], 1.0], ['<=', ['get', 'popularity'], 10.0]], '#000004', ['all', ['>', ['get', 'popularity'], 10.0], ['<=', ['get', 'popularity'], 100.0]], '#2d115f', ['all', ['>', ['get', 'popularity'], 100.0], ['<=', ['get', 'popularity'], 1000.0]], '#721f81', ['all', ['>', ['get', 'popularity'], 1000.0], ['<=', ['get', 'popularity'], 10000.0]], '#b6377a', ['all', ['>', ['get', 'popularity'], 10000.0], ['<=', ['get', 'popularity'], 100000.0]], '#f1605d', ['all', ['>', ['get', 'popularity'], 100000.0], ['<=', ['get', 'popularity'], 1000000.0]], '#feaf78', ['all', ['>', ['get', 'popularity'], 1000000.0], ['<=', ['get', 'popularity'], 10000000.0]], '#fcfdbf', '#ffffff']}
        }
],
}