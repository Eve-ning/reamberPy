![license](https://img.shields.io/github/license/Eve-ning/reamberPy)
![dls](https://img.shields.io/pypi/dm/reamber)
![codecov-coverage](https://img.shields.io/codecov/c/github/Eve-ning/reamberPy)
![codefactor](https://img.shields.io/codefactor/grade/github/Eve-ning/reamberPy)
![version](https://img.shields.io/pypi/v/reamber)

# Reamber (Py) 

[:blue_book: Wiki](https://eve-ning.github.io/reamberPy/index.html) & [Getting Started](https://eve-ning.github.io/reamberPy/info/GettingStarted.html)

`pip install reamber`

------

VSRG Toolbox for data extraction, manipulation & analysis.

# Features

- Game Support: osu!mania, StepMania, BMS and partially O2Jam files.
- Algorithms: Map IO, Conversion, Map Image Generation, Pattern Extraction
- Data Architecture: Pandas DataFrame Integration

> This is built on pandas `DataFrame`, thus, if you need more control, you can 
retrieve the underlying `DataFrame` via the `.df` property on many reamber classes. 

# Status

This is in alpha, names and references will change without notice.
We highly recommended to fix version in requirements.

## For Developers, By Developers

A growing amount of osu!mania players are interested in programming.
The best way to learn is to relate it to something that you're familiar with.

That's why I'm making a library that allows you to tamper with your favorite
games, and learn on the way.

# Migrating to >v0.1.1 Releases

Migrating to `>0.1.1` means spending time updating **a lot** of names.

Major changes in `0.1.1` include many differences in naming. 
Only update it if you don't plan mind spending time refactoring.
