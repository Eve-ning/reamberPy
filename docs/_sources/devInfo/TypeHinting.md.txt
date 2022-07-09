# Type Hinting

This article outlines how Type Hinting works in reamberPy.

Unlike most strongly-typed languages, Python is weakly typed, and the IDE must go great lengths to guess the correct
data type for auto-complete suggestions.

However, as a programmer, you can override the suggestions by giving explicit hints

```python
def alpha(self):
    return self._alpha
```

Here, if ``alpha`` is not known to the IDE, it'll give useless hints.

```python
def alpha(self) -> str:
    return self._alpha
```

Adding a return value will force the IDE to assume it's an ``str``, thus showing warnings for invalid ``str``
operations.

## Decorator Conflicts

I use decorators extensively to reduce repeated code via meta-programming.

**Pre-decorated**

```py
@generate_funcs
class Alpha: ...


@generate_funcs
class AlphaNew: ...
```

**Post-decorated**

```python
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
```

These decorators can **generate** new functions, however, the IDE cannot detect its return type as it's too deeply
nested.

Simply put, decorator-generated functions don't type-hint.

While we can redefine them, it defeats the purpose of decorator-generated functions. This is solved with **stub
headers**.

## Python Stubs `.pyi`

In some languages you define headers with type hints, then define implementation in its body. This is possible with
Python too with **stub** ``.pyi`` files.

``alpha.pyi``

```py
class Alpha:
    def alpha(self) -> str: ...
```

``alpha.py``

```py
class Alpha:
    def alpha(self):
        return self._alpha
```

Combining **Decorators** with **Python Stubs**, you can create a simple code-base with extensive type-hinting.

### Important Notes

``.pyi`` files are **never** executed, that means, even if it yields an error, the package can still run.

As decorators break the type-hinting, ``.pyi`` should avoid having ``@decorators`` unless the IDE can support it
internally, such as ``@dataclass``.

## Templating

Templating reduces the hinting of inheritables.

For example, using ``Generic``

```py
from typing import Generic, TypeVar

T = TypeVar('T')


class Alpha(Generic[T]):
    def alpha(self) -> T:
        return self._alpha


class Beta(Alpha[int]):
    ...
```

Yields

```py
class Beta(Alpha):
    def alpha(self) -> int:
        return self._alpha
```

This is useful in propagating new types forward.

