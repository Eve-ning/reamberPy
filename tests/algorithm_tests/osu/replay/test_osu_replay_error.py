import pickle
from pathlib import Path

from reamber.algorithms.osu.OsuReplayError import osu_replay_error
from tests.conftest import MAPS_DIR, REPS_OSU_DIR

MAP_PATH = MAPS_DIR / "osu/MAGiCVLGiRL_ZVPH.osu"
REPS_PATH = REPS_OSU_DIR / "MAGiCVLGiRL_ZVPH.osu/"

PKL_PATH = Path(__file__).parent / "errors.pkl"


def test_replay():
    errors = osu_replay_error(
        sorted([r.as_posix() for r in REPS_PATH.glob("*.osr")]),
        MAP_PATH.as_posix()
    )
    with open(PKL_PATH, "rb+") as f:
        errors_exp = pickle.load(f)

    for act, exp in zip(errors.errors, errors_exp.errors):
        for ar_act, ar_exp in zip(act.hits.values(), exp.hits.values()):
            assert all(ar_act == ar_exp)

        for ar_act, ar_exp in zip(act.releases.values(),
                                  exp.releases.values()):
            assert all(ar_act == ar_exp)
