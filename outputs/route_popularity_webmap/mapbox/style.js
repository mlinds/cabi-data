
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
            "paint": {'line-width': ['case', ['all', ['>=', ['get', 'popularity'], 1.0], ['<=', ['get', 'popularity'], 3.162278]], 4.5, ['all', ['>', ['get', 'popularity'], 3.162278], ['<=', ['get', 'popularity'], 10.0]], 4.5, ['all', ['>', ['get', 'popularity'], 10.0], ['<=', ['get', 'popularity'], 31.622777]], 4.5, ['all', ['>', ['get', 'popularity'], 31.622777], ['<=', ['get', 'popularity'], 100.0]], 4.5, ['all', ['>', ['get', 'popularity'], 100.0], ['<=', ['get', 'popularity'], 316.227766]], 4.5, ['all', ['>', ['get', 'popularity'], 316.227766], ['<=', ['get', 'popularity'], 1000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 1000.0], ['<=', ['get', 'popularity'], 3162.27766]], 4.5, ['all', ['>', ['get', 'popularity'], 3162.27766], ['<=', ['get', 'popularity'], 10000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 10000.0], ['<=', ['get', 'popularity'], 31622.776602]], 4.5, ['all', ['>', ['get', 'popularity'], 31622.776602], ['<=', ['get', 'popularity'], 100000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 100000.0], ['<=', ['get', 'popularity'], 316227.766017]], 4.5, ['all', ['>', ['get', 'popularity'], 316227.766017], ['<=', ['get', 'popularity'], 1000000.0]], 4.5, ['all', ['>', ['get', 'popularity'], 1000000.0], ['<=', ['get', 'popularity'], 3162277.660168]], 4.5, ['all', ['>', ['get', 'popularity'], 3162277.660168], ['<=', ['get', 'popularity'], 10000000.0]], 4.5, 0], 'line-opacity': ['case', ['all', ['>=', ['get', 'popularity'], 1.0], ['<=', ['get', 'popularity'], 3.162278]], 1.0, ['all', ['>', ['get', 'popularity'], 3.162278], ['<=', ['get', 'popularity'], 10.0]], 1.0, ['all', ['>', ['get', 'popularity'], 10.0], ['<=', ['get', 'popularity'], 31.622777]], 1.0, ['all', ['>', ['get', 'popularity'], 31.622777], ['<=', ['get', 'popularity'], 100.0]], 1.0, ['all', ['>', ['get', 'popularity'], 100.0], ['<=', ['get', 'popularity'], 316.227766]], 1.0, ['all', ['>', ['get', 'popularity'], 316.227766], ['<=', ['get', 'popularity'], 1000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 1000.0], ['<=', ['get', 'popularity'], 3162.27766]], 1.0, ['all', ['>', ['get', 'popularity'], 3162.27766], ['<=', ['get', 'popularity'], 10000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 10000.0], ['<=', ['get', 'popularity'], 31622.776602]], 1.0, ['all', ['>', ['get', 'popularity'], 31622.776602], ['<=', ['get', 'popularity'], 100000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 100000.0], ['<=', ['get', 'popularity'], 316227.766017]], 1.0, ['all', ['>', ['get', 'popularity'], 316227.766017], ['<=', ['get', 'popularity'], 1000000.0]], 1.0, ['all', ['>', ['get', 'popularity'], 1000000.0], ['<=', ['get', 'popularity'], 3162277.660168]], 1.0, ['all', ['>', ['get', 'popularity'], 3162277.660168], ['<=', ['get', 'popularity'], 10000000.0]], 1.0, 0], 'line-color': ['case', ['all', ['>=', ['get', 'popularity'], 1.0], ['<=', ['get', 'popularity'], 3.162278]], '#000004', ['all', ['>', ['get', 'popularity'], 3.162278], ['<=', ['get', 'popularity'], 10.0]], '#0e0b2a', ['all', ['>', ['get', 'popularity'], 10.0], ['<=', ['get', 'popularity'], 31.622777]], '#281158', ['all', ['>', ['get', 'popularity'], 31.622777], ['<=', ['get', 'popularity'], 100.0]], '#481078', ['all', ['>', ['get', 'popularity'], 100.0], ['<=', ['get', 'popularity'], 316.227766]], '#681b81', ['all', ['>', ['get', 'popularity'], 316.227766], ['<=', ['get', 'popularity'], 1000.0]], '#862781', ['all', ['>', ['get', 'popularity'], 1000.0], ['<=', ['get', 'popularity'], 3162.27766]], '#a6327d', ['all', ['>', ['get', 'popularity'], 3162.27766], ['<=', ['get', 'popularity'], 10000.0]], '#c63c74', ['all', ['>', ['get', 'popularity'], 10000.0], ['<=', ['get', 'popularity'], 31622.776602]], '#e34e65', ['all', ['>', ['get', 'popularity'], 31622.776602], ['<=', ['get', 'popularity'], 100000.0]], '#f56c5c', ['all', ['>', ['get', 'popularity'], 100000.0], ['<=', ['get', 'popularity'], 316227.766017]], '#fc9065', ['all', ['>', ['get', 'popularity'], 316227.766017], ['<=', ['get', 'popularity'], 1000000.0]], '#feb57c', ['all', ['>', ['get', 'popularity'], 1000000.0], ['<=', ['get', 'popularity'], 3162277.660168]], '#fed99b', ['all', ['>', ['get', 'popularity'], 3162277.660168], ['<=', ['get', 'popularity'], 10000000.0]], '#fcfdbf', '#ffffff']}
        }
],
}