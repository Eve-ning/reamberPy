import json
from pathlib import Path

import pandas as pd

from reamber.algorithms.osu.parse_replay import parse_replays_error, parse_replay_actions
from reamber.osu import OsuMap
from tests.conftest import MAPS_DIR, REPS_OSU_DIR

MAP_PATH = MAPS_DIR / "osu/MAGiCVLGiRL_ZVPH.osu"
REPS_PATH = list((REPS_OSU_DIR / "MAGiCVLGiRL_ZVPH.osu/").glob("*.osr"))[:2]
N_REPS = len(REPS_PATH)
PKL_PATH = Path(__file__).parent / "errors.pkl"
osu = OsuMap.read_file(MAP_PATH.as_posix())


def test_parse_replay_action_osr():
    print(REPS_PATH)
    df_actions = parse_replay_actions(replay=REPS_PATH[0], keys=4, src='file')
    assert isinstance(df_actions, pd.DataFrame)


def test_parse_replays_error_osr():
    df_errors = parse_replays_error(
        {r.as_posix(): r.as_posix() for r in REPS_PATH},
        osu=osu, src="file"
    )
    cat_counts = df_errors.category.value_counts()
    assert cat_counts['Hit'] == len(osu.hits) * N_REPS
    assert cat_counts['Hold Head'] == len(osu.holds) * N_REPS
    assert cat_counts['Hold Tail'] == len(osu.holds) * N_REPS


def test_parse_replays_error_osr_infer():
    df_errors = parse_replays_error(
        {r.as_posix(): r.as_posix() for r in REPS_PATH},
        osu=osu, src="infer"
    )
    cat_counts = df_errors.category.value_counts()
    assert cat_counts['Hit'] == len(osu.hits) * N_REPS
    assert cat_counts['Hold Head'] == len(osu.holds) * N_REPS
    assert cat_counts['Hold Tail'] == len(osu.holds) * N_REPS


def test_parse_replays_error_api():
    with open(Path(__file__).parent / "response.json", "r") as f:
        data = json.load(f)

    df_errors = parse_replays_error({'rep1': data['content']}, osu=osu, src='api')
    cat_counts = df_errors.category.value_counts()
    assert cat_counts['Hit'] == len(osu.hits)
    assert cat_counts['Hold Head'] == len(osu.holds)
    assert cat_counts['Hold Tail'] == len(osu.holds)


def test_parse_replays_error_api_infer():
    with open(Path(__file__).parent / "response.json", "r") as f:
        data = json.load(f)

    df_errors = parse_replays_error({'rep1': data['content']}, osu=osu, src='infer')
    cat_counts = df_errors.category.value_counts()
    assert cat_counts['Hit'] == len(osu.hits)
    assert cat_counts['Hold Head'] == len(osu.holds)
    assert cat_counts['Hold Tail'] == len(osu.holds)
