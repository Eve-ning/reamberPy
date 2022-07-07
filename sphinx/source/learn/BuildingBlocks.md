# Building Blocks of ReamberPy

On top of the 5 game classes, we have a `Base` class.

This class implements all common functionality across all game classes.

For example:

- `QuaHit`
- `OsuHit`
- `SMHit`
- `O2JHit`
- `BMSHit`

All derives from `Hit`. This means, all of them have offset.

Thus, you can expect that `QuaHitList(...).offset` & `OsuHitList(...).offset` to behave the same.

## Singular & List types

For most `Type` classes, there's an associated `TypeList` class.

For example, `OsuHold` has a `OsuHoldList`. They behave similarly, however, one is a list.

- `OsuHold(...).offset` will yield a single value
- `OsuHoldList(...).offset` will yield a list of values

## Properties

Usually, if it exists, then it'll be implemented.

For example:

`OsuHold` will implement:

- `offset`, the LN Head
- `tail_offset`, the LN Tail
- `length`, the LN length
- `column`, the column of the note.

Thus, they can be simply accessed via `.___` syntax.

## Pandas-like Operations

A great feature of ReamberPy objects is that they can be broadcasted to.

For example

- `OsuHoldList(...).offset += 1000` will add 1 second to all objects
- `OsuBpmList(...).bpm += 100` will add 100 to all BPMs

In fact, the underlying data representation is pandas' `DataFrame`!.

## Next Steps

After the basics, it's time to deal with actual maps.

**[Previous Tutorial: Basics](Basics)**
**[Next Tutorial: Working With Maps](WorkingWithMaps)**
