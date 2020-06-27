#################
Osu Measure Lines
#################

*This algorithm is targeted at osu! only. This is sub-optimal if you're dealing with a game that allows negative BPMs.*

osu! only allows measure lines to move forward, never backward. The trick to make them move freely is to repeatedly
refresh the screen with new positions.

This is almost analogous to the phenomenon that if a fan spins fast enough, it'll look like it's spinning backwards.
It's the reverse-rotation effect.

All of these algorithms use this phenomenon but there are important differences!

Not required, but it's to have a good understanding on how Measure Line manipulation is done.

Read the following if you're unfamiliar.

.. toctree::
   :maxdepth: 1

    Measure Line Manipulation Primer <svOsuMeasureLinePrimer>

***********
Differences
***********

Recommendations
===============

I heavily recommend Algorithm B, which uses a Hybrid algorithm to create the smoothest measure line animation available.

Algorithm A uses only Bpm Lines, however they have flickering on multi-function inputs.

Traits
======

**Version A**

- Multi-Function Stacking.
- Returns a SvPkg
- Often flickers on multi-function, generates noise. (Other random measure lines)

The version attempts to stack functions together to create a longer frame.

**Version B**

- Multi-Function Stacking
- Sv + Bpm Hybrid
- Returns a List of OsuSvObj and OsuBpmObj
- Rarely flickers on multi-function, doesn't generate noise. (No other random measure lines)

This version uses a singular BPM every frame to define how many measure lines should exist.

Structures
==========

*Algorithm Annotation is explained in the info page*::

    All symbols are defined as 1 ms length unless specified.

    T     : Teleport (999999... BPM)
    S     : Stop     (0.000...1 BPM)
    F     : Function (This determines where the line should be)
    _     : Empty    (This is just to pad the sequence)
    {X}...: Repeat X (This is determined by the user input)

**Version A**

- ``S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,...``

**Version B**

- ``S{_}...D{F},S{_}...D{F}_,S{_}...D{F}_,...`` Algorithm
- ``D`` is a specially calculated teleport
- ``{F}`` is defined in OsuSliderVelocities, and is all collapsed in 1ms.

Parameters
----------

All functions take similar parameters and all parameters have the same function.

First & Last Offset
^^^^^^^^^^^^^^^^^^^

The offsets to start and end the function

Functions (funcs)
^^^^^^^^^^^^^^^^^

The functions to use. It expects a float as an input and output.

For example, if you want a measure line moving upwards::

    funcs = [lambda x: x * 40000]

The value 40000 is a multiplier so that it's visible on the screen.

If you want measure lines that cross each other::

    funcs = [lambda x: x * 40000, lambda x: 40000 - x * 40000]

Note that if ``BPM == 0``, it'll resort to the ``FALLBACK_ZERO_BPM defined in each class``.

You can have as many functions as you want, but both **Version 1 and 2** will generate more noise the more functions
you have.

Teleport, Stop, Reference and Fill Bpm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Teleport Bpm specifies the value of BPM used to clear the screen. (Only Algo A)
- Stop Bpm specifies the value of BPM used to stop the scroll.
- End Bpm specifies the BPM used to end the algorithm.
- Reference Bpm specifies the current BPM osu! is used to center all BPMs.
    - It is the value displayed in brackets. E.g. **BPM: 100-400(200)** reference is 200.
- Fill Bpm specifies the value of BPM used to fill the rest of the bounds if the sequence length does not perfectly fit.
    - Fill Bpm can be ``None``, that is, it will not fill.

Start & End X
^^^^^^^^^^^^^

The X values to linearly skim through when calculating the Bpms required.

***********
Module Info
***********

.. automodule:: reamber.algorithms.generate.sv.generators.svOsuMeasureLineA
.. automodule:: reamber.algorithms.generate.sv.generators.svOsuMeasureLineB
