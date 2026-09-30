import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plt_temp import make_dataframe


def test_make_dataframe():
    data = {
        "hourly": {
            "time": [
                "2026-09-30T00:00",
                "2026-09-30T01:00",
            ],
            "temperature_2m": [
                10.5,
                11.2,
            ],
        }
    }

    df = make_dataframe(data)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["time", "temperature_c"]
    assert len(df) == 2
    assert df["temperature_c"].tolist() == [10.5, 11.2]