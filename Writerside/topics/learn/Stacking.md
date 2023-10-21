# Stacking

> **Stacking joins all tables together regardless of type.**
> {style="note"}

## Example

An example of a Hit List

| offset | column | 
|--------|--------|
| 1000   | 2      | 
| 2000   | 3      | 
| 4000   | 1      |

An example of a Hold List

| offset | column | length |
|--------|--------|--------|
| 1000   | 3      | 100    |
| 2000   | 2      | 200    |
| 3500   | 3      | 500    |

An example of a Bpm List

| offset | bpm | metronome |
|--------|-----|-----------|
| 1000   | 200 | 4         |

If we stacked them, we yield::

| offset | column | length | bpm | metronome |
|--------|--------|--------|-----|-----------|
| 1000   | 3      | 100    |     |           |
| 2000   | 2      | 200    |     |           |
| 3500   | 3      | 500    |     |           |
| 1000   | 2      |        |     |           |
| 2000   | 3      |        |     |           |
| 4000   | 1      |        |     |           |
| 1000   |        |        | 200 | 4         |

This allows us to modify **all** matching properties at one go.

> Note that empty cells are `NaN`.

> If you're familiar with `pd.DataFrame`, basic operations such as `+=`, `/=`
> work here.
> {style="note"}

Here's how to use `stack` to add offset to everything.


<tabs>
    <tab title="osu!mania">
        <code-block lang="python">
from reamber.osu.OsuMap import OsuMap
m = OsuMap.read_file(...)
s = m.stack()
s.offset += 100
</code-block>
    </tab>
    <tab title="Quaver">
        <code-block lang="python">
from reamber.quaver.QuaMap import QuaMap
m = QuaMap.read_file(...)
s = m.stack()
s.offset += 100
</code-block>
    </tab>
    <tab title="BMS">
<code-block lang="python">
from reamber.bms import BMSMap
m = BMSMap.read_file(...)
s = m.stack()
s.offset += 100
</code-block>
    </tab>
    <tab title="Stepmania">
<code-block lang="python">
from reamber.sm import SMMapSet
ms = SMMapSet.read_file(...)
s = ms.stack()
s.offset += 100
</code-block>
    </tab>
    <tab title="O2Jam">
<code-block lang="python">
from reamber.o2jam import O2JMapSet
ms = O2JMapSet.read_file(...)
s = ms.stack()
s.offset += 100
</code-block>
    </tab>
</tabs>

## Including

If you only wanted to change `hits` column only, you can pass it as an argument

```python
from reamber.osu import OsuMap
from reamber.osu.lists.notes import OsuHitList

m = OsuMap.read_file("my_map.osu")
s = m.stack([OsuHitList])
```

> Note that including only some classes will remove some properties
>
> E.g. The above will not have `length` property despite type-hinting
> showing it is available.
> {style="warning"}

## Conditional Stacking

**Condition Stacking only works on Map, not Mapset, see below for workaround**

If you're familiar with `pd.DataFrame`, you can do something like

```python
import pandas as pd

df = pd.DataFrame(...)
df.loc[df.offset < 1000, 'column'] += 1
```

This adds column by 1 where `df.offset` is less than 1000.

For stacking, you **MUST** also do it through `loc`.

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
stack.loc[stack.offset < 1000, 'column'] += 1
```

Do not do it through the property.

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
# Don't do this
stack.column[stack.offset < 1000] += 1
```

This raises a `SettingWithCopy` warning!
This means, it might not have updated the `stack` by reference.

## MapSet Stacking Caveats

When stacking with `MapSet` s, it will return a `pd.DataFrame` of the `Map`
stack results. Due to copying caveats, conditional stacking will not work,
loop through the maps and set individually.

```python
from reamber.sm import SMMapSet

ms = SMMapSet.read_file("...")
stack = ms.stack()
stack.offset *= 2
```

If you want **conditional stacking**, loop and `loc`.

```python
from reamber.sm import SMMapSet

ms = SMMapSet.read_file("...")
for m in ms:
    s = m.stack()
    s.loc[s.offset > 1000, 'column'] += 2
```

## More Examples

To get acquainted with this, here are some additional examples. Learning this
will be equivalent to learning
`pd.DataFrame` conditional slicing and setting.

We assume `stack = m.stack()`, where `m` is a map if not specified.

### First and Last Offsets {collapsible="true"}

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
first, last = stack.offset.min(), (stack.offset + stack.length).max()
```

Note that indexing will yield a `pd.Series`.

### Reversing Columns {collapsible="true"}

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
keys = stack.column.max()
stack.column *= -1
stack.column += keys
```

### Getting Columns Conditionally by Offset {collapsible="true"}

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
cols = stack.loc[stack.offset >= 10000, 'column']
```

### Multiple Conditions {collapsible="true"}

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
stack.loc[(stack.column == 2) & (stack.offset > 1000), 'column']
```

### Multiple Properties {collapsible="true"}

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
stack.loc[(stack.column == 2) &
          (stack.offset > 1000), ['column', 'offset']] *= 2
```

## SettingWithCopy Warning

*If you're running into this issue, see above.*

> [This is due to chained indexing](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy)
>

In short, when we write

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
stack.column[stack.offset < 1000] += 1
```

It expands to

```python
from reamber.osu import OsuMap

stack = OsuMap.read_file("...").stack()
stack_copy = stack.__getitem__('column')
stack_copy[stack.offset < 1000] += 1
```

Notice that `stack_copy` may or may not be a copy, thus, it may not update
the `stack`.

