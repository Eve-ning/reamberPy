# osu! Replay Error

This algorithm finds hit/release errors of a replay.

```py
from reamber.algorithms.osu.OsuReplayError import osu_replay_error

errors = osu_replay_error(
    [
        "path/to/replay0.osr",
        "path/to/replay1.osr",
        "path/to/replay2.osr",
    ], "path/to/map.osu"
)
```

## Returns `ManiaHitErrorEvents`

As per the example above, ``errors`` is a ``ManiaHitErrorEvents`` instance.

```py
from reamber.algorithms.osu.OsuReplayError import osu_replay_error

errors = osu_replay_error([...], ...)

replays_errors = errors.errors

map_offsets = errors.map_offsets
replays_offsets = errors.reps_offsets
```

To retrieve the errors of the first replay:
- `replay_0_error = replays_errors[0]`

You may then retrieve its hit / release error: 
- `hits = replay_0_error.hits` 
- `releases = replay_0_error.releases`

For a specific key's error:
- `hit_0: np.ndarray = hits[0]`
- `releases_1: np.ndarray = releases[1]`

## Details

The algorithm finds the minimum error between each replay action & map object.

Thus, it's not an exact simulation of the replay.

You will likely find differences in in-game results if the map is very dense.


