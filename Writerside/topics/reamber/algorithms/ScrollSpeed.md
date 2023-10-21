# Scroll Speed

<tldr>
    <p>Computes the effective, relative scroll speed to the dominant bpm</p>
</tldr>

The dominant bpm is the bpm that is the most active in the map.
See [Dominant BPM](DominantBpm.md) for more information.

> This also considers SVs. It will multiply the scroll speed with it.
{style="note"}

## Return

Returns a `pd.Series` of name `speed`, with the `offset` as the index.

## Usage

<tabs>
    <tab title="osu!mania">
        <code-block lang="python">
        from reamber.algorithms.analysis import scroll_speed
        from reamber.osu import OsuMap
        import pandas as pd&#xA;
        osu_map = OsuMap.read_file(&quot;path/to/map.osu&quot;)
        s: pd.Series = scroll_speed(osu_map)
        offset = s.index
        </code-block>
    </tab>
    <tab title="Quaver">
        <code-block lang="python">
        from reamber.algorithms.analysis import scroll_speed
        from reamber.qua import QuaMap
        import pandas as pd&#xA;
        qua_map = QuaMap.read_file(&quot;path/to/map.qua&quot;)
        s: pd.Series = scroll_speed(qua_map)
        offset = s.index
        </code-block>
    </tab>
</tabs>


