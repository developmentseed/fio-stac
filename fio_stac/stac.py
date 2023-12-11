"""Create STAC Item from a vector dataset."""

import datetime
import warnings
from contextlib import ExitStack
from typing import Dict, List, Optional, Tuple, Union

import fiona
import pystac
from fiona.model import to_dict
from fiona.transform import transform_geom

PROJECTION_EXT_VERSION = "v1.1.0"

EPSG_4326 = fiona.crs.CRS.from_epsg(4326)


try:
    import numpy
except ImportError:  # pragma: nocover
    rioxarray = None  # type: ignore


def bbox_to_geom(bbox: Tuple[float, float, float, float]) -> Dict:
    """Return a geojson geometry from a bbox."""
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [bbox[0], bbox[1]],
                [bbox[2], bbox[1]],
                [bbox[2], bbox[3]],
                [bbox[0], bbox[3]],
                [bbox[0], bbox[1]],
            ]
        ],
    }


def get_dataset_geom(
    src_dst: fiona.Collection,
    densify_pts: int = 0,
    precision: int = -1,
) -> Dict:
    """Get Raster Footprint."""
    if densify_pts < 0:
        raise ValueError("`densify_pts` must be positive")

    try:
        bounds = src_dst.bounds
    except fiona.errors.DriverError:
        bounds = None

    if src_dst.crs and bounds is not None:
        # 1. Create Polygon from raster bounds
        geom = bbox_to_geom(bounds)

        # 2. Densify the Polygon geometry
        if src_dst.crs != EPSG_4326 and densify_pts and numpy is not None:
            # Derived from code found at
            # https://stackoverflow.com/questions/64995977/generating-equidistance-points-along-the-boundary-of-a-polygon-but-cw-ccw
            coordinates = numpy.asarray(geom["coordinates"][0])

            densified_number = len(coordinates) * densify_pts
            existing_indices = numpy.arange(0, densified_number, densify_pts)
            interp_indices = numpy.arange(existing_indices[-1] + 1)
            interp_x = numpy.interp(interp_indices, existing_indices, coordinates[:, 0])
            interp_y = numpy.interp(interp_indices, existing_indices, coordinates[:, 1])
            geom = {
                "type": "Polygon",
                "coordinates": [[(x, y) for x, y in zip(interp_x, interp_y)]],
            }

        # 3. Reproject the geometry to "epsg:4326"
        geom = to_dict(
            transform_geom(
                src_dst.crs,
                EPSG_4326,
                geom,
                precision=precision,
                antimeridian_cutting=True,
            )
        )

        xs = []
        ys = []
        features = geom.get("features") or [geom]
        for _j, feat in enumerate(features):
            w, s, e, n = fiona.bounds(feat)
            xs.extend([w, e])
            ys.extend([s, n])

        bbox = (min(xs), min(ys), max(xs), max(ys))

    else:
        warnings.warn(
            "Input file doesn't have CRS information, setting geometry and bbox to (-180,-90,180,90)."
        )
        bbox = (-180.0, -90.0, 180.0, 90.0)
        geom = bbox_to_geom(bbox)

    return {"bbox": list(bbox), "footprint": geom}


def get_projection_info(src_dst: fiona.Collection) -> Dict:
    """Get projection metadata.

    The STAC projection extension allows for three different ways to describe the coordinate reference system
    associated with a raster :
    - EPSG code
    - WKT2
    - PROJJSON

    All are optional, and they can be provided altogether as well. Therefore, as long as one can be obtained from
    the data, we add it to the returned dictionary.

    see: https://github.com/stac-extensions/projection

    """
    projjson = None
    wkt2 = None
    epsg = None
    if src_dst.crs is not None:
        # EPSG
        epsg = src_dst.crs.to_epsg() if src_dst.crs.is_epsg_code else None

        # PROJJSON
        try:
            projjson = src_dst.crs.to_dict(projjson=True)
        except (AttributeError, TypeError) as ex:
            warnings.warn(f"Could not get PROJJSON from dataset : {ex}")
            pass

        # WKT2
        try:
            wkt2 = src_dst.crs.to_wkt()
        except Exception as ex:
            warnings.warn(f"Could not get WKT2 from dataset : {ex}")
            pass

    meta = {
        "epsg": epsg,
        "geometry": bbox_to_geom(src_dst.bounds),
        "bbox": list(src_dst.bounds),
    }

    if projjson is not None:
        meta["projjson"] = projjson

    if wkt2 is not None:
        meta["wkt2"] = wkt2

    return meta


def get_media_type(src_dst: fiona.Collection) -> Optional[str]:
    """Find MediaType for a vector dataset."""
    driver = src_dst.driver

    try:
        return pystac.MediaType[driver.upper()]
    except:  # noqa
        pass

    warnings.warn("Could not determine the media type from GDAL driver.")
    return None


def create_stac_item(
    source: str,
    input_datetime: Optional[datetime.datetime] = None,
    extensions: Optional[List[str]] = None,
    collection: Optional[str] = None,
    collection_url: Optional[str] = None,
    properties: Optional[Dict] = None,
    id: Optional[str] = None,
    assets: Optional[Dict[str, pystac.Asset]] = None,
    asset_name: Optional[str] = None,
    asset_roles: Optional[List[str]] = None,
    asset_media_type: Optional[Union[str, pystac.MediaType]] = "auto",
    asset_href: Optional[str] = None,
    with_proj: bool = False,
    geom_densify_pts: int = 0,
    geom_precision: int = -1,
) -> pystac.Item:
    """Create a Stac Item.

    Args:
        source (str): input path.
        input_datetime (datetime.datetime, optional): datetime associated with the item.
        extensions (list of str): input list of extensions to use in the item.
        collection (str, optional): name of collection the item belongs to.
        collection_url (str, optional): Link to the STAC Collection.
        properties (dict, optional): additional properties to add in the item.
        id (str, optional): id to assign to the item (default to the source basename).
        assets (dict, optional): Assets to set in the item. If set we won't create one from the source.
        asset_name (str, optional): asset name in the Assets object.
        asset_roles (list of str, optional): list of str | list of asset's roles.
        asset_media_type (str or pystac.MediaType, optional): asset's media type.
        asset_href (str, optional): asset's URI (default to input path).
        with_proj (bool): Add the `projection` extension and properties (default to False).
        geom_densify_pts (int): Number of points to add to each edge to account for nonlinear edges transformation (Note: GDAL uses 21).
        geom_precision (int): If >= 0, geometry coordinates will be rounded to this number of decimal.

    Returns:
        pystac.Item: valid STAC Item.

    """
    properties = properties or {}
    extensions = extensions or []
    asset_roles = asset_roles or []

    layers = fiona.listlayers(source)

    with fiona.open(source) as src_dst:
        item_id = id or src_dst.name
        asset_name = asset_name or src_dst.name

        dataset_geom = get_dataset_geom(
            src_dst,
            densify_pts=geom_densify_pts,
            precision=geom_precision,
        )

        media_type = (
            get_media_type(src_dst) if asset_media_type == "auto" else asset_media_type
        )

        if "start_datetime" not in properties and "end_datetime" not in properties:
            input_datetime = input_datetime or datetime.datetime.utcnow()

        # add projection properties
        if with_proj:
            extensions.append(
                f"https://stac-extensions.github.io/projection/{PROJECTION_EXT_VERSION}/schema.json",
            )

            properties.update(
                {
                    f"proj:{name}": value
                    for name, value in get_projection_info(src_dst).items()
                }
            )

    layer_schemas = {}
    for layer in layers:
        with fiona.open(source, layer=layer) as lyr_dst:
            schema = lyr_dst.schema
            layer_schemas.update({layer: schema})

    properties.update({"vector:layers": layer_schemas})

    # item
    item = pystac.Item(
        id=item_id,
        geometry=dataset_geom["footprint"],
        bbox=dataset_geom["bbox"],
        collection=collection,
        stac_extensions=extensions,
        datetime=input_datetime,
        properties=properties,
    )

    # if we add a collection we MUST add a link
    if collection:
        item.add_link(
            pystac.Link(
                pystac.RelType.COLLECTION,
                collection_url or collection,
                media_type=pystac.MediaType.JSON,
            )
        )

    # item.assets
    if assets:
        for key, asset in assets.items():
            item.add_asset(key=key, asset=asset)

    else:
        item.add_asset(
            key=asset_name,
            asset=pystac.Asset(
                href=asset_href or source,
                media_type=media_type,
                roles=asset_roles,
            ),
        )

    return item
