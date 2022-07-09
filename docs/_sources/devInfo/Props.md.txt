# Properties

reamberPy uses decorators that create "properties", I will explain its process and uses here.

As outlined in the :doc:`Development Info <DevInfo>`, most objects use a ``pd.Series`` or ``pd.DataFrame`` data source.

Note that you get its columns with attributes and indexing.

```py
import pandas as pd

srs: pd.Series
assert srs.offset == srs['offset']

df: pd.DataFrame
assert df.offset == df['offset']
```

This is crucial in creating decorators to index these as **properties**

## Why Pandas

Pandas is an extension of NumPy with useful column-based operations, suitable for this. While I could've customized my
own library, it'll be too much of a liability of maintenance.

It provides excellent functions, on top of its indexing, with good performance on correct usage.

## Item Prop Decorators

The custom ``Property`` decorators grabs the class' attribute ``_props`` and generates useful functions.

For example

```py
from reamber.base import item_props
from reamber.osu import OsuTimingPointMeta
from reamber.base.Timed import Timed


@item_props()
class OsuSv(OsuTimingPointMeta, Timed):
    _props = dict(multiplier=['float', 1.0])
```

Here, ``@item_props()`` grabs ``_props`` and generates the following functions

```py
from reamber.osu import OsuTimingPointMeta
from reamber.base.Timed import Timed
import pandas as pd


class OsuSv(OsuTimingPointMeta, Timed):
    @property
    def multiplier(self) -> pd.Series:
        return self.data['multiplier']

    @multiplier.setter
    def multiplier(self, val) -> None:
        self.data['multiplier'] = val
```

Looking at ``OsuSv.pyi``, you can see the stub implementations, which type hints these without its body.

## List Prop Decorators

Similar to Item Prop Decorators, this affects lists

For example,

```py
from reamber.base.Property import list_props
from reamber.osu.OsuSv import OsuSv
from reamber.base.lists.TimedList import TimedList


@list_props(OsuSv)
class OsuSvList(TimedList[OsuSv]):
    ...
```

It will generate the following class.

```python
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSv import OsuSv
import pandas as pd


class OsuSvList(TimedList[OsuSv]):

    @property
    def multiplier(self) -> pd.Series:
        return self.df['multiplier']

    @multiplier.setter
    def multiplier(self, val) -> None:
        self.df['multiplier'] = val
```

Without meta-programming decorators, this would have caused many consistency issues.
