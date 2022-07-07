from reamber.algorithms.osu.OsuReplayError import OsuReplayError
from tests.unit_tests.conftest import MAPS_DIR, REPS_OSU_DIR

MAP_PATH = MAPS_DIR / "osu/MAGiCVLGiRL_ZVPH.osu"
REPS_PATH = REPS_OSU_DIR / "MAGiCVLGiRL_ZVPH.osu/"


def test_replay():
    ore = OsuReplayError(
        [r.as_posix() for r in REPS_PATH.glob("*.osr")],
        MAP_PATH.as_posix()
    )
    a = ore.errors()
