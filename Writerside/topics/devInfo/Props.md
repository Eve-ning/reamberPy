# Generating Properties on the Fly

reamberPy uses decorators that create "properties".

As outlined in the [Type Hinting](TypeHinting.md)`, most objects use `
pd.Series` or
`pd.DataFrame` data classes. One trick with these is that they can be indexed
with `[]` or `.`.

```python
import pandas as pd

srs: pd.Series
assert srs.offset == srs['offset']

df: pd.DataFrame
assert df.offset == df['offset']
```

<deflist collapsible="true" default-state="collapsed">
<def title="Why Pandas?">
Pandas is an extension of NumPy with useful column-based operations, suitable
for this. While I could've customized my
own library, it'll be too much of a liability of maintenance.

It provides excellent functions, on top of its indexing, with good performance
on correct usage.
</def>
</deflist>

## Item Prop Decorators

The custom `Property` decorators grabs the class' attribute `_props` and
generates the functions.

For example, `@item_props()` uses `_props` and generates the following
functions.

<tabs>
    <tab title="Pre-Decorated">
        <code-block lang="python">
        from reamber.base import item_props
        from reamber.osu import OsuTimingPointMeta
        from reamber.base.Timed import Timed
            @item_props()
            class OsuSv(OsuTimingPointMeta, Timed):
                _props = dict(multiplier=['float', 1.0])
        </code-block>
    </tab>
    <tab title="Post-Decorated">
        <code-block lang="python">
        from reamber.osu import OsuTimingPointMeta
        from reamber.base.Timed import Timed
        import pandas as pd
        class OsuSv(OsuTimingPointMeta, Timed):
            @property
            def multiplier(self) -&gt; pd.Series:
                return self.data['multiplier']
            @multiplier.setter
            def multiplier(self, val) -&gt; None:
                    self.data['multiplier'] = val
        </code-block>
    </tab>
</tabs>

As shown, the dictionary automatically creates the property functions.

## List Prop Decorators

Similar to Item Prop Decorators, this affects lists

<tabs>
    <tab title="Pre-Decorated">
        <code-block lang="python">
        from reamber.base.Property import list_props
        from reamber.osu.OsuSv import OsuSv
        from reamber.base.lists.TimedList import TimedList
        @list_props(OsuSv)
        class OsuSvList(TimedList[OsuSv]):
            ...
        </code-block>
    </tab>
    <tab title="Post-Decorated">
        <code-block lang="python">
        from reamber.base.lists.TimedList import TimedList
        from reamber.osu.OsuSv import OsuSv
        import pandas as pd
        class OsuSvList(TimedList[OsuSv]):
            @property
            def multiplier(self) -&gt; pd.Series:
                return self.df['multiplier']
            @multiplier.setter
            def multiplier(self, val) -&gt; None:
                self.df['multiplier'] = val
        </code-block>
    </tab>
</tabs>

As shown, it uses the `OsuSv` class' dictionary to generate the property
functions.

> Without meta-programming decorators, this would have caused many consistency
> issues.
{style='note'}
