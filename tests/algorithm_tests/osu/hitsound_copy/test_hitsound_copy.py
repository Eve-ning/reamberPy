from pathlib import Path

from pandas._testing import assert_frame_equal

from reamber.algorithms.osu.hitsound_copy import hitsound_copy
from reamber.osu import OsuMap
from reamber.osu.lists.notes import OsuHoldList

THIS_DIR = Path(__file__).parent


def test_hitsound_copy():
    source = OsuMap.read_file(THIS_DIR / "source.osu")
    target = OsuMap.read_file(THIS_DIR / "target.osu")

    result = hitsound_copy(source, target)

    assert_frame_equal(
        result.holds[["offset", "column", "length"]]
        .df.sort_values(["offset", "column"])
        .reset_index(drop=True),
        target.holds[["offset", "column", "length"]]
        .df.sort_values(["offset", "column"])
        .reset_index(drop=True),
        check_like=True,
    )

    assert_frame_equal(
        result.hits[["offset", "column"]]
        .df.sort_values(["offset", "column"])
        .reset_index(drop=True),
        target.hits[["offset", "column"]]
        .df.sort_values(["offset", "column"])
        .reset_index(drop=True),
        check_like=True,
    )


def test_hitsound_copy_nolns():
    # Supposed to replicate the no 'length' attribute condition, however, can't be replicated?
    source = OsuMap.read_file(THIS_DIR / "source.osu")
    target = OsuMap.read_file(THIS_DIR / "target.osu")

    source.holds = OsuHoldList([])
    target.holds = OsuHoldList([])
    result = hitsound_copy(source, target)

    assert_frame_equal(
        result.hits[["offset", "column"]]
        .df.sort_values(["offset", "column"])
        .reset_index(drop=True),
        target.hits[["offset", "column"]]
        .df.sort_values(["offset", "column"])
        .reset_index(drop=True),
        check_like=True,
    )
