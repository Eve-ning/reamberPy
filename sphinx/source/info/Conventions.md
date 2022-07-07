# Conventions

## Units

Unless specifically specified. The units used for the package are

| Unit of | Unit as          |
|---------|------------------|
| Time    | Milliseconds     |
| BPM     | Beats Per Minute |
| Column  | Integer from 0   |

There are multiple methods available in ``reamber.base.RAConst`` for conversion

- ``hr_to_min(hours)``
- ``hr_to_sec(hours)``
- ``hr_to_msec(hours)``
- ``min_to_hr(mins)``
- ...

## Map & MapSet

A MapSet contains Maps.

## Notes

``Note`` s can be either a ``Hit`` or ``Hold``.

``Note`` is the parent of those two.

This naming convention is used because it's easier to differentiate.

## BPM Points

I don't use ``TimingPoint`` because it's confusing.

