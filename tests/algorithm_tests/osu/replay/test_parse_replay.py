import json
from pathlib import Path

from reamber.algorithms.osu.parse_replay import parse_replays_error, parse_replay_actions
from reamber.osu import OsuMap
from tests.conftest import MAPS_DIR, REPS_OSU_DIR

MAP_PATH = MAPS_DIR / "osu/MAGiCVLGiRL_ZVPH.osu"
REPS_PATH = list((REPS_OSU_DIR / "MAGiCVLGiRL_ZVPH.osu/").glob("*.osr"))[:2]
PKL_PATH = Path(__file__).parent / "errors.pkl"
osu = OsuMap.read_file(MAP_PATH.as_posix())


def test_parse_replays_error_osr():
    errors = parse_replays_error(
        {r.as_posix(): r.as_posix() for r in REPS_PATH},
        osu=osu, src="file"
    )


def test_parse_replay_action_osr():
    errors = parse_replay_actions(
        replay=REPS_PATH[0],
        keys=4,
        src='file'
    )


def test_parse_replay_error_api():
    with open(Path(__file__).parent / "response.json", "r") as f:
        data = json.load(f)

    parse_replays_error({'rep1': data['content']}, osu=osu, src='api')
