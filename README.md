# fio-stac

<p align="center">
  <img src="https://user-images.githubusercontent.com/10407788/111794250-696da080-889c-11eb-9043-5bdc3aadb8bf.png" alt="fio-stac"></a>
</p>
<p align="center">
  <em>Create STAC Items from vector datasets.</em>
</p>
<p align="center">
  <a href="https://github.com/developmentseed/fio-stac/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/developmentseed/fio-stac/workflows/CI/badge.svg" alt="Test">
  </a>
  <a href="https://codecov.io/gh/developmentseed/fio-stac" target="_blank">
      <img src="https://codecov.io/gh/developmentseed/fio-stac/branch/main/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/fio-stac" target="_blank">
      <img src="https://img.shields.io/pypi/v/fio-stac?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypistats.org/packages/fio-stac" target="_blank">
      <img src="https://img.shields.io/pypi/dm/fio-stac.svg" alt="Downloads">
  </a>
  <a href="https://github.com/developmentseed/fio-stac/blob/main/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/developmentseed/fio-stac.svg" alt="Downloads">
  </a>
</p>

---

**Documentation**: <a href="https://developmentseed.github.io/fio-stac/" target="_blank">https://developmentseed.github.io/fio-stac/</a>

**Source Code**: <a href="https://github.com/developmentseed/fio-stac" target="_blank">https://github.com/developmentseed/fio-stac</a>

---

`fio-stac` is a simple [rasterio](https://github.com/mapbox/rasterio) plugin for creating valid STAC items from a raster dataset. The library is built on top of [pystac](https://github.com/stac-utils/pystac) to make sure we follow the STAC specification.

## Installation

```bash
$ pip install pip -U

# From Pypi
$ pip install fio-stac

# Or from source
$ pip install git+http://github.com/developmentseed/fio-stac
```

### Example

```json
// fio stac zip+https://naciscdn.org/naturalearth/10m/cultural/ne_10m_roads_north_america.zip | jq
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "ne_10m_roads_north_america",
  "properties": {
    "proj:epsg": 4326,
    "proj:geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [
            -176.7640084731439,
            14.590750676565
          ],
          [
            -52.64725244187383,
            14.590750676565
          ],
          [
            -52.64725244187383,
            70.2966838677457
          ],
          [
            -176.7640084731439,
            70.2966838677457
          ],
          [
            -176.7640084731439,
            14.590750676565
          ]
        ]
      ]
    },
    "proj:bbox": [
      -176.7640084731439,
      14.590750676565,
      -52.64725244187383,
      70.2966838677457
    ],
    "proj:projjson": {
      "$schema": "https://proj.org/schemas/v0.4/projjson.schema.json",
      "type": "GeographicCRS",
      "name": "WGS 84",
      "datum": {
        "type": "GeodeticReferenceFrame",
        "name": "World Geodetic System 1984",
        "ellipsoid": {
          "name": "WGS 84",
          "semi_major_axis": 6378137,
          "inverse_flattening": 298.257223563
        }
      },
      "coordinate_system": {
        "subtype": "ellipsoidal",
        "axis": [
          {
            "name": "Geodetic latitude",
            "abbreviation": "Lat",
            "direction": "north",
            "unit": "degree"
          },
          {
            "name": "Geodetic longitude",
            "abbreviation": "Lon",
            "direction": "east",
            "unit": "degree"
          }
        ]
      },
      "id": {
        "authority": "EPSG",
        "code": 4326
      }
    },
    "proj:wkt2": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AXIS[\"Latitude\",NORTH],AXIS[\"Longitude\",EAST],AUTHORITY[\"EPSG\",\"4326\"]]",
    "datetime": "2023-12-08T20:32:26.343189Z"
  },
  "geometry": {
    "coordinates": [
      [
        [
          -176.7640084731439,
          14.590750676565
        ],
        [
          -52.64725244187383,
          14.590750676565
        ],
        [
          -52.64725244187383,
          70.2966838677457
        ],
        [
          -176.7640084731439,
          70.2966838677457
        ],
        [
          -176.7640084731439,
          14.590750676565
        ]
      ]
    ],
    "type": "Polygon"
  },
  "links": [],
  "assets": {
    "asset": {
      "href": "/vsizip/vsicurl/https://naciscdn.org/naturalearth/10m/cultural/ne_10m_roads_north_america.zip",
      "roles": []
    }
  },
  "bbox": [
    -176.7640084731439,
    14.590750676565,
    -52.64725244187383,
    70.2966838677457
  ],
  "stac_extensions": [
    "https://stac-extensions.github.io/projection/v1.1.0/schema.json"
  ]
}
```

See https://developmentseed.org/fio-stac/intro/ for more.

## Contribution & Development

See [CONTRIBUTING.md](https://github.com/developmentseed/fio-stac/blob/main/CONTRIBUTING.md)

## Authors

See [contributors](https://github.com/developmentseed/fio-stac/graphs/contributors)

## Changes

See [CHANGES.md](https://github.com/developmentseed/fio-stac/blob/main/CHANGES.md).

## License

See [LICENSE](https://github.com/developmentseed/fio-stac/blob/main/LICENSE)