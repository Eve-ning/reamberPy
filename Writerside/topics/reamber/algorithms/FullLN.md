# Full LN

<tldr>
    <p>Converts a map into a Full LN Map.</p>
</tldr>

> This is not the same as inversing
> {style="note"}

## Usage

Convert a map to a Full LN:

<tabs>
    <tab title="osu!mania">
        <code-block lang="python">
        from reamber.algorithms.generate import full_ln
        from reamber.osu.OsuMap import OsuMap&#xA;
        osu = OsuMap.read_file(&quot;my_map.osu&quot;)
        osu2 = full_ln(osu, gap=150, ln_as_hit_thres=100)
        osu2.write_file(&quot;new_map.osu&quot;)
        </code-block>
    </tab>
    <tab title="Quaver">
        <code-block lang="python">
        from reamber.algorithms.generate import full_ln
        from reamber.quaver.QuaMap import QuaMap&#xA;
        qua = QuaMap.read_file(&quot;my_map.qua&quot;)
        qua2 = full_ln(qua, gap=150, ln_as_hit_thres=100)
        qua2.write_file(&quot;new_map.qua&quot;)
        </code-block>
    </tab>
</tabs>

> It doesn't work with `MapSet`s. Loop through the `MapSet` to convert
{style="warning"}

## Params

{style="narrow"}

gap
: Gap between an LN Tail and the next note.

ln_as_hit_thres
: Smallest LN length before it's converted to a hit.

### Example

Given `gap=150, ln_as_hit_thres=100`:

- If the distance between 2 notes is 250ms a 100ms LN is rendered.
- If the distance between 2 notes is 249ms there won't be a 99ms LN rendered 
  as `ln_as_hit_thres=100`. Instead, a `Hit` will be rendered.

