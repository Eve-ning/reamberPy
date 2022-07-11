import pytest

from reamber.osu.OsuNoteMeta import OsuNoteMeta


@pytest.mark.parametrize(
    "x_axis, keys, expected",
    [
        (-1, 4, 0), (0, 4, 0), (1, 4, 0), (127, 4, 0),
        (128, 4, 1), (129, 4, 1), (255, 4, 1),
        (256, 4, 2), (257, 4, 2), (383, 4, 2),
        (384, 4, 3), (385, 4, 3), (511, 4, 3), (512, 4, 3), (513, 4, 3)]
)
def test_x_axis_to_column_4k(x_axis, keys, expected):
    assert OsuNoteMeta.x_axis_to_column(x_axis, keys) == expected


@pytest.mark.parametrize(
    "x_axis, keys, expected",
    [
        (-1, 7, 0), (0, 7, 0), (1, 7, 0), (72, 7, 0), (73, 7, 0),
        (74, 7, 1), (145, 7, 1), (146, 7, 1),
        (147, 7, 2), (218, 7, 2), (219, 7, 2),
        (220, 7, 3), (291, 7, 3), (292, 7, 3),
        (293, 7, 4), (364, 7, 4), (365, 7, 4),
        (366, 7, 5), (437, 7, 5), (438, 7, 5),
        (439, 7, 6), (511, 7, 6), (512, 7, 6), (513, 7, 6)
    ]
)
def test_x_axis_to_column_7k(x_axis, keys, expected):
    assert OsuNoteMeta.x_axis_to_column(x_axis, keys) == expected
