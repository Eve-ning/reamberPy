SV Osu Measure Lines
====================

*This algorithm is targeted at osu! only. This is sub-optimal if you're dealing with a game that allows negative BPMs.*

osu! only allows measure lines to move forward, never backward. The trick to make them move freely is to repeatedly
refresh the screen with new positions.

This is almost analogous to the phenomenon that if a fan spins fast enough, it'll look like it's spinning backwards.
It's the reverse-rotation effect.

Leaving details for another page, this page will talk about how to use this function.

.. toctree::
   :maxdepth: 1

    Osu Measure Line Info <svOsuMeasureLineInfo>

Version 1 vs Version 2
----------------------

There is a small difference between version 1 and version 2. I recommend version 1 however.

*{A} means A repeats user-defined amount of times*

**Version 1**

- ``S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,...`` Algorithm.
- Multi-Function Stacking.

The version attempts to stack functions together to create a longer frame.

**Version 2**

- ``T_S{S}...F,T_S{S}...F,T_S{S}...F,...`` Algorithm.
- Multi-Function Flickering.

This version attempts to quickly swap around functions to "fake" that multiple functions are present at the same time.

Parameters
----------

Both functions take the same parameters and all parameters have the same function.

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

Note that if ``BPM == 0``, it'll resort to the ``FALLBACK_ZERO_BPM = 0.000000001``.

You can have as many functions as you want, but both **Version 1 and 2** will generate more noise the more functions
you have.

Teleport, Stop and Fill Bpm
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Teleport Bpm specifies the value of BPM used to clear the screen.
- Stop Bpm specifies the value of BPM used to stop the scroll.
- Fill Bpm specifies the value of BPM used to fill the rest of the bounds if the sequence length does not perfectly fit.
    - Fill Bpm can be ``None``, that is, it will not fill.

Start & End X
^^^^^^^^^^^^^

The X values to linearly skim through when calculating the Bpms required.

.. automodule:: reamber.algorithms.generate.sv.generators.svOsuMeasureLine
