import json
from pathlib import Path

import pandas as pd
import pytest

from reamber.algorithms.osu.parse_replay import (
    parse_replays_error,
    parse_replay_actions,
)
from reamber.osu import OsuMap
from tests.conftest import MAPS_DIR, REPS_OSU_DIR

MAP_PATH = MAPS_DIR / "osu/MAGiCVLGiRL_ZVPH.osu"
REPS_PATH = list((REPS_OSU_DIR / "MAGiCVLGiRL_ZVPH.osu/").glob("*.osr"))[:2]
N_REPS = len(REPS_PATH)
PKL_PATH = Path(__file__).parent / "errors.pkl"
osu = OsuMap.read_file(MAP_PATH.as_posix())


def test_parse_replay_action_osr():
    df_actions = parse_replay_actions(replay=REPS_PATH[0], keys=4, src="file")
    assert isinstance(df_actions, pd.DataFrame)


@pytest.mark.parametrize("src", ("file", "infer"))
@pytest.mark.xfail(reason="Not sure why this fails on GitHub Actions")
def test_parse_replays_error_osr(src: str):
    df_errors = parse_replays_error(
        {r.as_posix(): r.as_posix() for r in REPS_PATH}, osu=osu, src=src
    )
    cat_counts = df_errors.category.value_counts()
    assert cat_counts["Hit"] == len(osu.hits) * N_REPS
    assert cat_counts["Hold Head"] == len(osu.holds) * N_REPS
    assert cat_counts["Hold Tail"] == len(osu.holds) * N_REPS

    # There shouldn't be any misses within the replay, there are still some errors in the parsing due to estimation.
    assert df_errors.loc[df_errors.error.abs() > 100].empty


@pytest.mark.parametrize("src", ("api", "infer"))
def test_parse_replays_error_api(src: str):
    with open(Path(__file__).parent / "response.json", "r") as f:
        data = json.load(f)

    df_errors = parse_replays_error({"rep1": data["content"]}, osu=osu, src=src)
    cat_counts = df_errors.category.value_counts()
    assert cat_counts["Hit"] == len(osu.hits)
    assert cat_counts["Hold Head"] == len(osu.holds)
    assert cat_counts["Hold Tail"] == len(osu.holds)
