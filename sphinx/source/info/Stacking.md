# Stacking

**Stacking joins all tables together regardless of type.**

If you're not familiar with `pd.DataFrame`, take a look at how it represents 2D Data.

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
 
| offset | column   | length | bpm | metronome |
|--------|----------|--------|-----|-----------|
| 1000   | 3        | 100    |     |           |
| 2000   | 2        | 200    |     |           |
| 3500   | 3        | 500    |     |           |
| 1000   | 2        |        |     |           |
| 2000   | 3        |        |     |           |
| 4000   | 1        |        |     |           |
| 1000   |          |        | 200 | 4         |

This allows us to modify **all** matching properties at one go.

> Note that empty cells are `NaN`.

If you're familiar with `pd.DataFrame`, basic operations such as `+=`, `/=` work here.

Here's how to use ``stack`` to add offset to everything.

```py
from reamber.osu.OsuMap import OsuMap

m = OsuMap.read_file("path/to/file.osu")
stack = m.stack()

stack.offset += 1000

m.write_file("path/to/out.osu")
```

## Properties

Generally, if there exists a property, then it'll be included via the type-hint provided by your IDE.

For example, if your map has SVs, then `m.stack().multiplier` should be a valid call.

## Including

If you only wanted to change `hits` column only, you can pass it as an argument

```py
stack = m.stack(['hits'])
stack.offset += 1000
```

Note that the argument **MUST** be a list, not just a ``string``.

### KeyError

Note that including only some classes will remove some properties

```py
stack = m.stack('hits')
length = stack.length
```

This will raise a ``KeyError``, despite type-hinting showing it is available.

## Conditional Stacking

**Condition Stacking only works on Map, not Mapset, see below for workaround**

If you're familiar with ``pd.DataFrame``, you can do something like

```py
df.loc[df.offset < 1000, 'column'] += 1
```

This adds column by 1 where ``df.offset`` is less than 1000.

For stacking, you can, and **MUST** do it similarly.

```py
stack = m.stack()
stack.loc[stack.offset < 1000, 'column'] += 1
```

Note that the following is **invalid**

```py
stack = m.stack()
stack.column[stack.offset < 1000] += 1
```

This raises a ``SettingWithCopy`` warning!
This means, it might not have updated the ``stack`` by reference.

## MapSet Stacking Caveats

When stacking with ``MapSet`` s, it will return a ``pd.DataFrame`` of the ``Map`` stack results.

Because of copying caveats, conditional stacking will not work, loop through the maps and set individually.

This following will work

```python
ms = MapSet.read_file("...")
stack = ms.stack()
stack.offset *= 2
```

If you want **conditional stacking**, loop and ``loc``.

```py
ms = MapSet.read_file("...")
for m in ms:
    s = m.stack()
    s.loc[s.offset > 1000, 'column'] += 2
```

## More Examples

To get acquainted with this, here are some additional examples. Learning this will be equivalent to learning
``pd.DataFrame`` conditional slicing and setting.

We assume ``stack = m.stack()``, where ``m`` is a map if not specified.

### First and Last Offsets

```py
first, last = stack.offset.min(), (stack.offset + stack.length).max()
```

Note that indexing will yield a ``pd.Series``.

### Reversing Columns

```py
keys = stack.column.max()
stack.column *= -1
stack.column += keys
```

### Getting Columns Conditionally by Offset

```py
cols = stack.loc[stack.offset >= 10000, 'column']
```

### Multiple Conditions

```py
stack.loc[(stack.column == 2) & (stack.offset > 1000), 'column']
```

### Multiple Properties

```py
stack.loc[(stack.column == 2) & (stack.offset > 1000), ['column', 'offset']] *= 2
```

## SettingWithCopy Warning

*If you're running into this issue, see above.*

`This is due to chained indexing <https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy>`_

In short, when we write

```py
stack = m.stack()
stack.column[stack.offset < 1000] += 1
```

It expands to

```py
stack = m.stack()
stack_copy = stack.__getitem__('column')
stack_copy[stack.offset < 1000] += 1
```
Notice that ``stack_copy`` may or may not be a copy, thus, it may not update the ``stack``.
