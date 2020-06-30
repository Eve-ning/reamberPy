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

********
Examples
********

Algorithm A
===========

.. math::

    \begin{align*}
    f(x) &= 0.5 * \sin(2\pi x) + 0.5 \\
    g(x) &= 0.5 * \sin(2\pi x + \pi) + 0.5 \\
    \end{align*}

.. plot::
   :context: reset
   :include-source: False

   import matplotlib.pyplot as plt
   from math import pi
   import numpy as np

.. plot::
   :context:
   :align: center
   :width: 100%
   :include-source: False

   x = np.linspace(0, 4, 200)
   fig, ax = plt.subplots()
   ax.plot(x, 0.5 * np.sin(2 * pi * x) + 0.5)
   ax.plot(x, 0.5 * np.sin(2 * pi * x + pi) + 0.5)
   ax.set_aspect('equal')
   ax.grid(True, which='both')

   ax.axhline(y=0, color='k')
   ax.axvline(x=0, color='k')
   fig.tight_layout()
   plt.show()

.. code-block:: python
   :linenos:

    from reamber.osu.OsuBpm import OsuBpm
    from reamber.algorithms.generate.sv.generators.svOsuMeasureLineA import svOsuMeasureLineA
    from math import sin, pi

    seq = svOsuMeasureLineA(firstOffset=5000,
                            lastOffset=20000,
                            funcs=[lambda x: 0.5 * sin(x * pi * 2),
                                   lambda x: 0.5 * sin(x * pi * 2 + pi)],
                            fillBpm=200, startX=0, endX=4, endBpm=200, referenceBpm=200,
                            paddingSize=20).combine()

    with open("out.txt", "w+") as f:
        f.writelines([i.writeString() + "\n" for i in seq.writeAsBpm(OsuBpm)])

- Starts from **5000ms**, ends at **20000ms**.
- We have **2 sine functions**, as shown above.
- We start from :math:`x=0` to :math:`x=4`.
- Reference Bpm is used to match the peak of the sine wave to the top of the field
- If the algorithm doesn't perfectly end at **19999ms**, it'll add ``fillBpm`` Bpm objects until **19999ms**.
- We end off the algorithm with a **200Bpm** at **20000ms**.
- In each frame we have **20 extra empty milliseconds** as padding.

Algorithm B
===========

Same function input as Algorithm A.

Note the difference in output.

.. code-block:: python
   :linenos:

    from reamber.algorithms.generate.sv.generators.svOsuMeasureLineB import svOsuMeasureLineB
    from math import sin, pi

    lis = svOsuMeasureLineB(firstOffset=0,
                            lastOffset=40000,
                            funcs=[lambda x: 0.5 * sin(x * pi * 2),
                                   lambda x: 0.5 * sin(x * pi * 2 + pi)],
                            fillBpm=200, startX=0, endX=4, endBpm=100, referenceBpm=200,
                            paddingSize=20)

    with open("out.txt", "w+") as f:
      f.writelines([i.writeString() + "\n" for i in lis])

- Starts from **0ms**, ends at **40000ms**.
- We have **2 sine functions**, as previously shown above.
- We start from :math:`x=0` to :math:`x=4`.
- Reference Bpm is used to match the peak of the sine wave to the top of the field
- If the algorithm doesn't perfectly end at **39999ms**, it'll add ``fillBpm`` Bpm objects until **39999ms**.
- We end off the algorithm with a **200Bpm** at **20000ms**.
- In each frame we have **20 extra empty milliseconds** as padding.

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
- No minimum distance that lines can be separated by.

The version attempts to stack functions together to create a longer frame.

**Version B**

- Multi-Function Stacking
- Sv + Bpm Hybrid
- Returns a List of OsuSv and OsuBpm
- Rarely flickers on multi-function, doesn't generate noise. (No other random measure lines)
- Has a small minimum distance that lines can be separated by. (Scales proportionally with Bpm)

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

**********
Parameters
**********

All functions take similar parameters and all parameters have the same function.

First & Last Offset
===================

The offsets to start and end the function

Functions (funcs)
=================

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
======================================

- Teleport Bpm specifies the value of BPM used to clear the screen. (Only Algo A)
- Stop Bpm specifies the value of BPM used to stop the scroll.
- End Bpm specifies the BPM used to end the algorithm.
- Reference Bpm specifies the current BPM osu! is used to center all BPMs.
    - It is the value displayed in brackets. E.g. **BPM: 100-400(200)** reference is 200.
- Fill Bpm specifies the value of BPM used to fill the rest of the bounds if the sequence length does not perfectly fit.
    - Fill Bpm can be ``None``, that is, it will not fill.

Start & End X
=============

The X values to linearly skim through when calculating the Bpms required.

***********
Module Info
***********

.. automodule:: reamber.algorithms.generate.sv.generators.svOsuMeasureLineA
.. automodule:: reamber.algorithms.generate.sv.generators.svOsuMeasureLineB
