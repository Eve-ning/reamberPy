# Conversions

<tldr>
    <p>Converts between Game Map Types</p>
</tldr>

> Converting is rather difficult, especially between maps that use millisecond
> and fractional snapping. If there are any issues, please do report them.
> {style="warning"}

## Syntax

The syntax is always consistent.

> There are many combinations, I will only show a few.

<tabs>
    <tab title="Quaver To StepMania">
        <code-block lang="python">
        from reamber.quaver.QuaMap import QuaMap
        from reamber.algorithms.convert import QuaToSM
        qua = QuaMap.read_file(&quot;file.qua&quot;)
        sm = QuaToSM.convert(qua)
        sm.write_file(&quot;file.sm&quot;)
        </code-block>
    </tab>
    <tab title="osu!mania to Quaver">
        <code-block lang="python">
        from reamber.osu.OsuMap import OsuMap
        from reamber.algorithms.convert import OsuToQua
        osu = OsuMap.read_file(&quot;file.osu&quot;)
        qua = OsuToQua.convert(osu)
        qua.write_file(&quot;file.qua&quot;)
        </code-block>
    </tab>
    <tab title="O2Jam to osu!mania">
        <code-block lang="python">
        from reamber.o2jam.O2JMapSet import O2JMapSet
        from reamber.algorithms.convert import O2JToOsu
        o2j = O2JMapSet.read_file(&quot;file.ojn&quot;)
        osu = O2JToOsu.convert(o2j)
        osu.write_file(&quot;file.osu&quot;)
        </code-block>
    </tab>
    <tab title="BMS to osu!mania">
        <code-block lang="python">
        from reamber.bms import BMSMap
        from reamber.algorithms.convert import BMSToOsu
        bms = BMSMap.read_file(&quot;file.bme&quot;)
        osu = BMSToOsu.convert(bms)
        osu.write_file(&quot;file.osu&quot;)
        </code-block>
    </tab>
</tabs>

> Note that converting to a game that uses `MapSet`, it will automatically
> cast any `Map` to a `MapSet`.
{style="note"}

> Most conversions will yield a bad offset, please do check them.
{style="warning"}
