import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_data_dictionary_covers_raw_columns():
    dictionary = pd.read_csv(ROOT / "data" / "schema" / "data_dictionary.csv")
    raw = pd.read_csv(ROOT / "data" / "raw" / "cpn" / "SPoS_MSC_v4_sensitivity_OFAT_2400.csv", nrows=1)
    assert set(dictionary["column"]) == set(raw.columns)


def test_datapackage_paths_exist_and_hash_format_is_sha256():
    package = json.loads((ROOT / "data" / "schema" / "datapackage.json").read_text(encoding="utf-8"))
    assert package["version"] == "4.0.0"
    assert len(package["resources"]) == 4
    for resource in package["resources"]:
        assert (ROOT / resource["path"]).exists()
        assert resource["hash"].startswith("sha256:")
        assert len(resource["hash"].split(":", 1)[1]) == 64
