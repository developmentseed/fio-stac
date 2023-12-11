
`fio-stac` can be used either from the command line as a rasterio plugin (`fio stac`) or from your own script.

For more information about the `Item` specification, please see https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md

# CLI

```
$ fio stac --help
Usage: fio stac [OPTIONS] INPUT

  Fiona STAC plugin: Create a STAC Item for Vector dataset.

Options:
  -d, --datetime TEXT             The date and time of the assets, in UTC (e.g
                                  2020-01-01, 2020-01-01T01:01:01).
  -e, --extension TEXT            STAC extension URL the Item implements.
  -c, --collection TEXT           The Collection ID that this item belongs to.
  --collection-url TEXT           Link to the STAC Collection.
  -p, --property NAME=VALUE       Additional property to add.
  --id TEXT                       Item id.
  -n, --asset-name TEXT           Asset name.
  --asset-href TEXT               Overwrite asset href.
  --asset-mediatype [COG|FLATGEOBUF|GEOJSON|GEOPACKAGE|GEOTIFF|HDF|HDF5|HTML|JPEG|JPEG2000|JSON|PNG|TEXT|TIFF|KML|XML|PDF|auto]
                                  Asset media-type.
  --with-proj / --without-proj    Add the 'projection' extension and
                                  properties.  [default: with-proj]
  --densify-geom INTEGER          Densifies the number of points on each edges
                                  of the polygon geometry to account for non-
                                  linear transformation.
  --geom-precision INTEGER        Round geometry coordinates to this number of
                                  decimal. By default, coordinates will not be
                                  rounded
  -o, --output PATH               Output file name
  --help                          Show this message and exit.
➜  fio-stac git:(main) ✗
```

### How To

The CLI can be run as is, just by passing a `source` vector data. You can also use options to customize the output STAC item:

- **datetime** (-d, --datetime)

    By design, all STAC items must have a datetime in their properties. By default the CLI will set the time to the actual UTC Time. The CLI will accept any format supported by [`dateparser`](https://dateparser.readthedocs.io/en/latest/).

    You can also define `start_datetime` and `end_datetime` by using `--datetime {start}/{end}` notation.

- **extension** (-e, --extension)

    STAC Item can have [extensions](https://github.com/radiantearth/stac-spec/tree/master/extensions) which indicates that the item has additional properties (e.g proj information). This option can be set multiple times.

    You can pass the extension option multiple times: `-e extension1 -e extension2`.

- **projection extension** (--with-proj / --without-proj)

    By default the `projection` extension and properties will be added to the item.

    link: https://github.com/stac-extensions/projection/

    ```json
    {
        "proj:epsg": 3857,
        "proj:geometry": {"type": "Polygon", "coordinates": [...]},
        "proj:bbox": [...],
        "proj:shape": [8192, 8192],
        "proj:transform": [...],
        "datetime": "2021-03-19T02:27:33.266356Z"
    }
    ```

    You can pass `--without-proj` to disable it.

- **collection** (-c, --collection)

    Add a `collection` attribute to the item.

- **collection link** (--collection-url)

    When adding a collection to the Item, the specification state that a Link must also be set. By default the `href` will be set with the collection id. You can specify a custom URL using this option.

- **properties** (-p, --property)

    You can add multiple properties to the item using `-p {KEY}={VALUE}` notation. This option can be set multiple times.

- **id** (--id)

    STAC Item id to set. Default to the source basename.

- **asset name** (-n, --asset-name)

    Name to use in the assets section. Default to `asset`.

    ```json
    {
        "asset": {
            "href": "my.geojson"
        }
    }
    ```

- **asset href** (--asset-href)

    Overwrite the HREF in the `asset` object. Default to the source path.

- **media type** (--asset-mediatype)

    Set the asset `mediatype`.

    If set to `auto`, `fio-stac` will try to find the mediatype.

- **geometry density** (--densify-geom)

    When creating the GeoJSON geometry from the input dataset we usually take the `bounding box` of the data and construct a simple Polygon which then get reprojected to EPSG:4326. Sadly the world is neither flat and square, so doing a transformation using bounding box can lead to non-ideal result. To get better results and account for nonlinear transformation you can add `points` on each edge of the polygon using `--densify-geom` option.

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
    "vector:layers": {
      "ne_10m_roads_north_america": {
        "properties": {
          "prefix": "str:5",
          "number": "str:5",
          "class": "str:10",
          "type": "str:12",
          "divided": "str:10",
          "country": "str:25",
          "state": "str:25",
          "note": "str:100",
          "scalerank": "int:4",
          "uident": "int:9",
          "length": "float:13.11",
          "rank": "int:4",
          "continent": "str:50"
        },
        "geometry": "LineString"
      }
    },
    "datetime": "2023-12-11T15:21:15.054810Z"
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
    "ne_10m_roads_north_america": {
      "href": "zip+https://naciscdn.org/naturalearth/10m/cultural/ne_10m_roads_north_america.zip",
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

```json
// fio stac zip+https://naciscdn.org/naturalearth/10m/cultural/ne_10m_roads_north_america.zip \
//   -d 2020-04-22 \
//   --without-proj \
//   -c myprivatecollection \
//   -p comments:name=myfile \
//   --id roads \
//   -n america \
//   --asset-href zip+https://naciscdn.org/naturalearth/10m/cultural/ne_10m_roads_north_america.zip | jq
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "roads",
  "properties": {
    "comments:name": "myfile",
    "vector:layers": {
      "ne_10m_roads_north_america": {
        "properties": {
          "prefix": "str:5",
          "number": "str:5",
          "class": "str:10",
          "type": "str:12",
          "divided": "str:10",
          "country": "str:25",
          "state": "str:25",
          "note": "str:100",
          "scalerank": "int:4",
          "uident": "int:9",
          "length": "float:13.11",
          "rank": "int:4",
          "continent": "str:50"
        },
        "geometry": "LineString"
      }
    },
    "datetime": "2020-04-22T00:00:00Z"
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
  "links": [
    {
      "rel": "collection",
      "href": "myprivatecollection",
      "type": "application/json"
    }
  ],
  "assets": {
    "america": {
      "href": "zip+https://naciscdn.org/naturalearth/10m/cultural/ne_10m_roads_north_america.zip",
      "roles": []
    }
  },
  "bbox": [
    -176.7640084731439,
    14.590750676565,
    -52.64725244187383,
    70.2966838677457
  ],
  "stac_extensions": [],
  "collection": "myprivatecollection"
}
```


# API

see: [api](api/fio_stac/stac.md)
