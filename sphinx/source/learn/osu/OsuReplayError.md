# osu! Parse Replay

This algorithm parses replay files/API responses into DataFrames. 
We also add another algorithm to find replay error with respect to a map. 

## Source

In both functions, the source should be specified, else can be inferred.

The source ``src`` argument can be either ``file``, ``api``, ``infer``.

For example

```python
import os
import requests

from reamber.algorithms.osu.parse_replay import parse_replay_actions

# File parsing
parse_replay_actions("path/to.osr", src="file", keys=7)

# API stream parsing
url = f'https://osu.ppy.sh/api/get_replay?k={os.environ["osu_api_key"]}&s=123456&m=3'
response = requests.get(url)
parse_replay_actions(response.json()['content'], src='api', keys=4)
```

## Replay Actions

```py
from reamber.algorithms.osu.parse_replay import parse_replay_actions

df_actions = parse_replay_actions("path/to.osr", src="file", keys=7)
```

The ``keys`` must be provided as it's not possible to find the keys without assumptions

### Return

DataFrame schema 

| offset | column | is_press | 
|--------|--------|----------|
| int    | int    | bool     | 

Each row describes an action of the replay, whether the player has released, or pressed, on a specific column, at what
offset. 

## Replay Error

We use the absolute minimum distance to match each replay action to its respective expected action in the map.

```py
from reamber.algorithms.osu.parse_replay import parse_replays_error
from reamber.osu import OsuMap

df_errors = parse_replays_error(
    replays={"rep1": "path/to1.osr", "rep2": "path/to2.osr"},
    osu=OsuMap.read_file("path/to.osu"),
    src="file"
)
```

The ``replays`` argument must be a dictionary, with key as the identifier for the returned index.
Think of the keys as the identifier of the replays.

### Return

DataFrame schema 

| replay_id (Index) | offset | column | is_press | error | 
|-------------------|--------|--------|----------|-------|
| object            | int    | int    | bool     | int   |

Each row describes the error of the note, the offset, column, whether it's a press or release, and the error in ms.

The index, ``replay_id`` is populated with respect to the dictionary keys provided in the function.

### Details

As it's a minimum absolute distance matching, it's not an exact simulation of the replay.

You will likely find differences in in-game results if the map is very dense.


