# osu! Parse Replay

<tldr>
    <p>Parse replay files/API responses into DataFrames.</p>
</tldr>

## Source

The source is a string that describes the source of the replay. which can
be either `file`, `api`, `infer`.

For example

<tabs>
    <tab title="From File">
        <code-block lang="python">
        from reamber.algorithms.osu.parse_replay import parse_replay_actions&#xA;
        parse_replay_actions(&quot;path/to.osr&quot;, src=&quot;file&quot;, keys=7)
        </code-block>
    </tab>
    <tab title="From API">
        <code-block lang="python">
        import os
        import requests&#xA;
        from reamber.algorithms.osu.parse_replay import parse_replay_actions&#xA;
        # API stream parsing
        url = f'https://osu.ppy.sh/api/get_replay?k={os.environ[&quot;osu_api_key&quot;]}&amp;s=123456&amp;m=3'
        response = requests.get(url)
        parse_replay_actions(response.json()['content'], src='api', keys=4)
        </code-block>
    </tab>
</tabs>

### Parse Replay Actions Return

DataFrame schema

{style="narrow"}

offset
: The offset of the action in ms.

column
: The column that the action is on.

is_press
: Whether the action is a press or release.

## Replay Error

We use the **absolute minimum distance** to match each replay action to its
respective expected action in the map.

> As it's a minimum absolute distance matching,
> it's not an exact simulation of the replay.
> You will likely find differences in in-game results if the map is very dense.
> {style="warning"}

```python
from reamber.algorithms.osu.parse_replay import parse_replays_error
from reamber.osu import OsuMap

df_errors = parse_replays_error(
    replays={"rep1": "path/to1.osr", "rep2": "path/to2.osr"},
    osu=OsuMap.read_file("path/to.osu"),
    src="file"
)
```

The `replays` argument must be a dictionary, with key as the identifier for the
returned index. Think of the keys as the identifier of the replays.

### Replay Error Return

DataFrame schema

{style="narrow"}

replay_id
: The identifier of the replay.

offset
: The offset of the action in ms.

column
: The column that the action is on.

is_press
: Whether the action is a press or release.

error
: The error in ms.
