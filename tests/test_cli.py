"""tests fio_stac.cli."""

import json
import os

from fio_stac.scripts.cli import stac

PREFIX = os.path.join(os.path.dirname(__file__), "fixtures")


def test_rio_stac_cli(runner):
    """Should work as expected."""
    with runner.isolated_filesystem():
        src_path = os.path.join(PREFIX, "coutwildrnp.shp")
        result = runner.invoke(stac, [src_path])
        assert not result.exception
        assert result.exit_code == 0
        stac_item = json.loads(result.output)
        assert stac_item["type"] == "Feature"
        assert stac_item["id"] == "coutwildrnp"
        assert stac_item["assets"]["coutwildrnp"]
        assert stac_item["assets"]["coutwildrnp"]["href"] == src_path
        assert stac_item["links"] == []
        assert stac_item["stac_extensions"] == [
            "https://stac-extensions.github.io/projection/v1.1.0/schema.json",
        ]
        assert "datetime" in stac_item["properties"]
        assert "proj:epsg" in stac_item["properties"]
