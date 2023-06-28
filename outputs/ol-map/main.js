import './style.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import GeoJSON from 'ol/format/GeoJSON.js';
import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import { Circle, Fill, Stroke, Style } from 'ol/style.js';
import TileImage from 'ol/source/TileImage.js';
import { plasma } from 'colormap/colorScale';

const network_layer = new VectorLayer({
  source: new VectorSource({
    url: "vectordata/network.json",
    format: new GeoJSON(),
  })
});

const station_layer = new VectorLayer({
  source: new VectorSource({
    url: "vectordata/station_data.json",
    format: new GeoJSON(),
    interactive: true
  }),
  style: new Style({
    image: new Circle({
      radius: 2,
      fill: new Fill({
        color: "red",
      }),
      stroke: new Stroke({
        color: "black",
        width: 0.1,
      }),
    }),
    zIndex: Infinity,
  }),
});

const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new TileImage({
        url: "http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
      }
      )
    }),
    network_layer,
    station_layer
  ],
  view: new View({
    center: [-8577497, 4712729],
    zoom: 11
  })
});


