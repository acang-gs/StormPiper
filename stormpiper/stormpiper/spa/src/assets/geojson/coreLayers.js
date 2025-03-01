// import { COORDINATE_SYSTEM } from "@deck.gl/core";
import { GeoJsonLayer, BitmapLayer } from "@deck.gl/layers";
import { TileLayer } from "@deck.gl/geo-layers";
// import { Matrix4 } from "math.gl";
/*
const wetlands = {
  layer: GeoJsonLayer,
  getData: () => vectorData.wetlands,
  props: {
    id: "wetlands",
    label: "Wetlands",
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};
const capitalProjectStreets = {
  layer: GeoJsonLayer,
  getData: () => vectorData.capitalProjectsStreets,
  props: {
    id: "capitalProjectStreets",
    label: "Capital Project Streets",
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};
const activeSWMain = {
  layer: GeoJsonLayer,
  getData: () => vectorData.activeSWMain,
  props: {
    id: "activeSWMain",
    label: "Active Surfacewater Main Lines",
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => {
      return parseInt(f.properties["DIAMETER"]) / 48;
    },
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};
const proposedSWFacility = {
  layer: GeoJsonLayer,
  getData: () => vectorData.proposedSWFacility,
  props: {
    id: "proposedSWFacility",
    label: "Proposed Surface Water Facilities",
    getPointRadius: 20,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 2,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};
const activeWWMain = {
  layer: GeoJsonLayer,
  getData: () => vectorData.activeWWMain,
  props: {
    id: "activeWWMain",
    label: "Active Wastewater Main Lines",
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};

// const esAll = {
//   layer: GeoJsonLayer,
//   data: "https://storage.googleapis.com/uwt-public/geojson/es_all.geojson",
//   props: {
//     id: "esAll",
//     label: "Test ES Cloud Layer",
//     getPointRadius: 10,
//     getFillColor: [160, 160, 180, 200],
//     getLineColor: [160, 160, 180, 200],
//     getDashArray: (f) => [20, 0],
//     getLineWidth: (f) => 1,
//     getElevation: (f) => 500,
//     lineWidthScale: 10,
//     lineWidthMinPixels: 1,
//     pickable: true,
//     dashJustified: true,
//     dashGapPickable: true,
//   },
// };

const row = {
  layer: GeoJsonLayer,
  getData: () => vectorData.row,
  props: {
    id: "row",
    label: "Right of Way",
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};
const equalOpportunityIndex = {
  layer: GeoJsonLayer,
  getData: () => vectorData.equalOpportunityIndex,
  props: {
    id: "equalOpportunityIndex",
    label: "Equal Opportunity Index",
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};
const landUseDesignations = {
  layer: GeoJsonLayer,
  getData: () => vectorData.landUseDesignations,
  props: {
    id: "landUseDesignations",
    label: "Land Use Designations",
    // coordinateSystem: COORDINATE_SYSTEM.METER_OFFSETS,
    // coordinateOrigin: [-126.8636967, 45.1517825, 0],
    // modelMatrix: new Matrix4().scale([0.2887,0.3374,1]),
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};
*/
const activeLocalSWFacility = {
  layer: GeoJsonLayer,
  props: {
    // data:"https://gis.cityoftacoma.org/arcgis/rest/services/ES/SurfacewaterNetwork/MapServer/21/query?where=1%3D1&outFields=*&returnGeometry=true&f=geojson&outSR=4326",
    data: "/api/rest/tmnt_facility/?f=geojson",
    id: "activeSWFacility",
    label: "Active Surface Water Facilities",
    getFillColor: [160, 160, 180, 0],
    getLineColor: [160, 160, 180, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    pickable: true,
    getPointRadius: 6,
    // pointRadiusUnits: "pixels",
    pointRadiusMaxPixels: 20,
    pointRadiusMinPixels: 6,
    // onClick:(info,event)=>console.log(info,event),
    highlightColor: [42, 213, 232],
    dashJustified: true,
    dashGapPickable: true,
    onByDefault: true,
  },
};

const delineations = {
  layer: GeoJsonLayer,
  props: {
    // data:"https://gis.cityoftacoma.org/arcgis/rest/services/ES/SurfacewaterNetwork/MapServer/21/query?where=1%3D1&outFields=*&returnGeometry=true&f=geojson&outSR=4326",
    data: "/api/rest/tmnt_delineation/?f=geojson",
    id: "tmnt_delineations",
    label: "Active Treatment Facility Upstream Delineations",
    getFillColor: [1, 1, 28, 1],
    defaultFillColor: [1, 1, 28, 1],
    getLineColor: [150, 130, 248, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => 1,
    getElevation: (f) => 500,
    lineWidthScale: 2,
    lineWidthMinPixels: 1,
    pickable: true,
    // onClick:(info,event)=>console.log(info,event),
    highlightColor: [42, 213, 232],
    dashJustified: true,
    dashGapPickable: true,
    onByDefault: false,
  },
};

const activeSWMain = {
  layer: GeoJsonLayer,
  // getData: () => vectorData.activeSWMain,
  props: {
    data: "https://gis.cityoftacoma.org/arcgis/rest/services/ES/SurfacewaterNetwork/MapServer/31/query?where=1%3D1&outFields=*&returnGeometry=true&f=geojson&outSR=4326",
    id: "activeSWMain",
    label: "Active Surfacewater Main Lines",
    getPointRadius: 10,
    getFillColor: [160, 160, 180, 200],
    getLineColor: [160, 160, 180, 200],
    getDashArray: (f) => [20, 0],
    getLineWidth: (f) => {
      return parseInt(f.properties["DIAMETER"]) / 48;
    },
    getElevation: (f) => 500,
    lineWidthScale: 10,
    lineWidthMinPixels: 1,
    pickable: true,
    dashJustified: true,
    dashGapPickable: true,
  },
};

const tssRaster = {
  layer: TileLayer,
  props: {
    id: "tssRaster",
    label: "Total Suspended Solids (TSS)",
    // data: "http://storage.googleapis.com/tnc-data-v1-bucket/TSSViz/{z}/{x}/{y}",
    // data:"./api/rest/tileserver/tnc_tss_ug_L/{z}/{x}/{y}/{s}",
    data: "/api/rest/tileserver/tnc_tss_ug_L/{z}/{x}/{y}/{s}",
    minZoom: 10,
    maxZoom: 18,
    tileSize: 256,

    renderSubLayers: (props) => {
      const {
        bbox: { west, south, east, north },
      } = props.tile;

      return new BitmapLayer(props, {
        data: null,
        image: props.data,
        bounds: [west, south, east, north],
      });
    },
  },
};
const landCoverRaster = {
  layer: TileLayer,
  props: {
    id: "landCoverRaster",
    label: "Land Cover Category",
    data: "http://storage.googleapis.com/ogd_map_tiles/landCover/{z}/{x}/{y}.png",
    // data:"./api/rest/tileserver/{{}}/{z}/{x}/{y}/{s}",
    minZoom: 10,
    maxZoom: 18,
    tileSize: 256,
    renderSubLayers: (props) => {
      const {
        bbox: { west, south, east, north },
      } = props.tile;

      return new BitmapLayer(props, {
        data: null,
        image: props.data,
        bounds: [west, south, east, north],
      });
    },
  },
};
const clusteredPopRaster = {
  layer: TileLayer,
  props: {
    id: "clusteredPopRaster",
    label: "Clustered Population",
    data: "http://storage.googleapis.com/ogd_map_tiles/clustered_pop/{z}/{x}/{y}.png",
    minZoom: 10,
    maxZoom: 18,
    tileSize: 256,
    renderSubLayers: (props) => {
      const {
        bbox: { west, south, east, north },
      } = props.tile;

      return new BitmapLayer(props, {
        data: null,
        image: props.data,
        bounds: [west, south, east, north],
      });
    },
  },
};

/* eslint-disable quote-props */
export const layerDict = {
  "Base Imagery": {
    Raster: [
      tssRaster,
      // landCoverRaster,
      // clusteredPopRaster
    ],
  },
  Surfacewater: {
    "Active Network": [
      delineations,
      // activeSWMain,
      activeLocalSWFacility,
    ],
  },
};
