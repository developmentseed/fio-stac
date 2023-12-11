"""test create_stac_item functions."""

import datetime
import os

import pytest

from fio_stac.stac import create_stac_item

PREFIX = os.path.join(os.path.dirname(__file__), "fixtures")
input_date = datetime.datetime.utcnow()


@pytest.mark.parametrize(
    "file",
    [
        "!test.geojson",
        "collection-pp.txt",
        "collection.txt",
        "coutwildrnp.shp",
        "coutwildrnp.zip",
        "curves_line.csv",
        "example.topojson",
        "gre.shp",
        "grenada.geojson",
        "issue627.geojson",
        "sequence-pp.txt",
        "sequence.txt",
        "test_gpx.gpx",
        "test_tin.csv",
        "test_tin.shp",
        "test_tz.geojson",
        "testopenfilegdb.gdb.zip",
    ],
)
def test_create_item(file):
    """Should run without exceptions."""
    src_path = os.path.join(PREFIX, file)
    if src_path.endswith(".zip"):
        src_path = f"zip+file://{src_path}"

    assert create_stac_item(
        src_path, input_datetime=input_date, with_proj=False
    ).validate()
