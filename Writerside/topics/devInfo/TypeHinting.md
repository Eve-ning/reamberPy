# Type Hinting Pandas Columns

> Understanding this isn't required to use the package, but it's useful to
> understand how the package works.

ReamberPy builds on top of Pandas, and as such, it uses Pandas' `DataFrame` to
index and store data. This allows for our object to yield columns via the
properties.

E.g. our `OsuMap` stores `bpms` as a `DataFrame`.

```python
from reamber.osu import OsuMap

m = OsuMap.read_file("path/to/file.osu")
bpms = m.bpms
```

Normally, we use `bpms["bpm"]` to access the column, however, we can also use
`bpms.bpm` to access the column. This works too in DataFrames, however, it is
never type-hinted.

ReamberPy works around this by performing meta-programming to not only
generate the appropriate properties functions, but also create
type-hinted `.pyi` stubs.

## Creating Properties via Decorators

We can create properties via decorators.

<tabs>
<tab title="Pre-Decorated">
<code-block lang="python">
@generate_funcs
class Alpha: ...
@generate_funcs
class AlphaNew: ...
</code-block>
</tab>
<tab title="Post-Decorated">
<code-block lang="python">
class Alpha:
    def to_beta(self):
        return self._alpha * 1.5
    def to_lambda(self):
        return self._alpha // 3
class AlphaNew:
    def to_beta(self):
        return self._alpha * 1.5
    def to_lambda(self):
        return self._alpha // 3
</code-block>
</tab>
</tabs>

These decorators **generates** the new functions, however, as a result of
decorators, the type-hints get broken. i.e. decorator-generated functions
can't type-hint.

## Python Stubs `.pyi`

To force type-hinting, we can create **Python Stubs** `.pyi` files.

<tabs>
<tab title=".py File">
<code-block lang="python">
class Alpha:
    def alpha(self) -&gt; str: ...
</code-block>
</tab>
<tab title=".pyi Stub File">
<code-block lang="python">
class Alpha:
    def alpha(self):
        return self._alpha
</code-block>
</tab>
</tabs>

Combining **Decorators** with **Python Stubs**, you can create a simple
code-base with extensive type-hinting.

> `.pyi` files are **never** executed, that means, even if it yields an error,
> the package can still run.
{style="note"}

## Templating

Templating reduces the hinting of inheritables.

For example, using `Generic`

```python
from typing import Generic, TypeVar

T = TypeVar('T')


class Alpha(Generic[T]):
    def alpha(self) -> T:
        return self._alpha


class Beta(Alpha[int]):
    ...
```

Yields

```python
class Beta(Alpha):
    def alpha(self) -> int:
        return self._alpha
```

This is useful in propagating new types forward.

