########################
Osu Measure Lines Primer
########################

****************
Acknowledgements
****************

I cannot fully list all osu!mania researchers that have put effort into discovering these methods. However, this guide
will not be possible without their contributions :)

*****
Intro
*****

To be able to understand how measure lines are created these are the pre-requisite knowledge required.

- How a BPM affects scroll speed
- What is the *reference* bpm

***************
Original Method
***************

To understand how it works, we go back to square one and revisit the phenomenon of a reversed Measure Line.

You cannot make a BPM Line go backwards, however we can trick players to thinking that it is.

Consider this animation::

    +   =========       =========        =========  TOP OF SCREEN
    [3] |       |       |       |        |-------|
    [2] |       |  -->  |-------|  -->   |       |
    [1] |-------|       |       |        |       |
    +   =========       =========        =========  HIT POSITION

We want to be able to move the measure line, from 1 to 2 to 3. The catch is that it's impossible with only a single
measure line.

Here's the first idea on how it is possible::

    [8] |       |       |       |        |       |
    [7] |       |       |       |        |-------|
    [6] |       |       |-------|  --+   |       |
    [5] |-------| --+   |       |    |   |       |
    [4] |       |   |   |       |  [1ms] |       |
    +   ========= [1ms] =========    |   =========  TOP OF SCREEN
    [3] |       |   |   |       |    +-> |-------|
    [2] |       |   +-> |-------|        |       |
    [1] |-------|       |       |        |       |
    +   =========       =========        =========  HIT POSITION

The idea is simple, within 1ms, we move the next measure line to the spot required.

However here are some things that we discovered when trying out this idea.

1. The lines don't render at all.
2. The lines don't exist long enough for the game to render it.
3. It's annoying to calculate the distance between the current and next Bpm Line

1ms Rule
========

If you have multiple BPM lines 1 ms after another, only the last one will render::

    OFFSET   [0][1][2][3][4][5][6][7][8][9][10]
    BPM LINE  X  X  X     X  X     X     X
    RENDERS         ^        ^     ^     ^

However, all lines will still function as normal.

Stop Motion
===========

The idea of stop motion is that you have enough time to see the current frame, however, not too long such that it feels
like a pause. Turns out that leaving the line at a spot for 1ms is way too short. So we need to somehow pause it

Consider the same pattern again::

    [8] |       |       |       |        |       |
    [7] |       |       |       |        |-------|
    [6] |       |       |-------|  --+   |       |
    [5] |-------| --+   |       |    |   |       |
    [4] |       |   |   |       |  [2ms] |       |
    +   ========= [2ms] =========    |   =========  TOP OF SCREEN
    [3] |       |   |   |       |    +-> |-------|
    [2] |       |   +-> |-------|        |       |
    [1] |-------|       |       |        |       |
    +   =========       =========        =========  HIT POSITION
    +   [  0ms  ]  -->  [02~20ms]  -->   [22~40ms]

If we can somehow pause the line at that particular spot for a few milliseconds, it should render correctly instead of
instantly disappearing.

Framing
=======

This is more of a personal preference, I feel that it's troublesome to find the ``[2ms]`` bpm required for every frame.

So what I do is that I refresh the whole screen with a Teleport BPM (a very high BPM Line)::

    +   =========       =========        =========       =========        =========   TOP OF SCREEN
    [3] |       |       |       |        |       |       |       |        |-------|<-TELEP
    [2] |       |       |       |        |-------|<-TELEP|       |        |       |
    [1] |-------|<-TELEP|       |        |       |       |       |        |       |
    +   =========       =========        =========       =========        =========   HIT POSITION
    +   [  0ms  ]  -->  [  1ms  ]  -->   [02~20ms]  -->  [  21ms ]  -->   [22~40ms]
    +   [STOPPED]       [ TELEP ]        [STOPPED]       [ TELEP ]        [STOPPED]
    +   [FRAME 0]                        [FRAME 1]                        [FRAME 2]

After every refresh, there's a stop to hold the frame.

********
Function
********

Every time you see a frame **VISUALLY**, these are the components::

    +   =========
    [3] |       |
    [2] |       |
    [1] |-------| Teleport Line
    +   ========= Function Line + Stop Line

How does the Function Line and Stop Line occur on the same spot? The stop line is actually so slow that both overlap::

    +   =========
    [3] |       |
    [2] |       |
    [1] |-------| Teleport Line [21ms / Inf Bpm]
    +   ========= Function Line [20ms / X Bpm] + Stop Line [0ms / 0 Bpm]

The final piece of the puzzle would be to find the value that the Function Line should hold such that the Teleport Line
occurs on ``[1]``.

With just simple math, if you get that correct value and multiply it by 2 and 3, you'd be able to move the Teleport Line
to ``[2]`` and ``[3]`` respectively.::

    +   =========
    [3] |       |
    [2] |-------| Teleport Line [21ms / Inf Bpm]
    [1] |       |
    +   ========= Function Line [20ms / 2X Bpm] + Stop Line [0ms / 0 Bpm]

    +   =========
    [3] |-------| Teleport Line [21ms / Inf Bpm]
    [2] |       |
    [1] |       |
    +   ========= Function Line [20ms / 3X Bpm] + Stop Line [0ms / 0 Bpm]

******************
Current Algorithms
******************

Algorithm A has been used widely in the early years of Measure Line Manipulation in osu!.
e.g. Backbeat Maniac, Singularity

The trick of Algorithm A is simpler in execution, hence it's more popular to be used.

The current improved Algorithm A is discovered because of the need to stack multiple functions together, creating a more
visually engaging chart.

Algorithm B is a proposed algorithm by `datoujia`, suggested to me by `Sillyp`. This algorithm proves to be the most
consistent zeroing out flickering. We'll discuss B much later.

Multi-function Stacking
=======================

Stacking is a problem encountered when handling multiple functions.

When you input multiple functions directly, you are essentially displaying

.. math::

    [A(x), A(x) + B(x), A(x) + B(x) + C(x) + ...]

this is because the algorithm places each function on top of each other.

To counter this, we need to subtract :math:`A(x)` from the next input, then :math:`B(x)` and so on.

However, you'd notice that if :math:`A(x) > B(x)` you'd end up with a negative result. Hence you'd need to consider the
order of the magnitudes.

Since the order of the input functions don't matter, we can order them at every :math:`x`.

For example

.. math::

    \begin{align*}
        A(x) &= sin(x) + 1 \\
        B(x) &= sin(x + \pi) + 1 \\
        C(x) &= 1 \\
    \end{align*}

With :math:`x=\pi/2` and :math:`x=3\pi/2`, you get the following orders.

.. math::

    \begin{align*}
        B(\pi/2) &< C(\pi/2) < A(\pi/2) \\
        A(3\pi/2) &< C(3\pi/2) < B(3\pi/2) \\
    \end{align*}

By ordering them from smallest to largest, you'd guarantee a non-negative result if you take the differences.

Negative Outputs
================

If the user decides to input a function that can output negatives

.. math::

    \begin{align*}
        A(x) &= sin(x) \\
        B(x) &= 1 \\
    \end{align*}

You'd run into a problem where the the algorithm may break. :math:`sin(3\pi/2) = -1`

The simplest solution would be to just add a ``max(f(x), 0)``. This is just a short form for ``if x < 0 then x = 0``.

Sequencing
==========

Sequencing takes some time to wrap your head around, it's just a short form on where to place parts::

    T     : Teleport (999999... BPM)
    S     : Stop     (0.000...1 BPM)
    F     : Function (This determines where the line should be)
    _     : Empty    (This is just to pad the sequence)
    {X}...: Repeat X (This is determined by the user input)

For Example::

    +       [0] [1] [2] [3] [4] | [5] [6] [7] [8] [9] | ...
    T_S_F =  T       S       F  |  T       S       F  | ...
            |||     |||     |||
       TELEPORT     STOP    FUNCTION

*************
Algo A Method
*************

This is mostly the same thing as discussed before, it's just an optimized version.

Assume Empty repeats 1 time, and there's 2 functions.::

    +                      [0] [1] [2] [3] [4] [5] [6] [7] [8] [9] | ...
    S_{_}...F{_F}..._S_T =  S           F1      F2      S       T  | ...

                       ... [10][11][12][13][14][15][16][17][18][19]
                       ...  S           F1      F2      S       T


*************
Algo B Method
*************

This method is largely different from A, we'll need to discover some new concepts.

Further Acknowledgements
========================

Inspired by datoujia's method.

Intro
=====

This method is largely different from A because it doesn't use BPM Lines to mark new measure lines, it utilizes
a High BPM to generate measure lines on each beat with a 1/4 metronome.

This can be packed together more tightly with a 0.01x SV.

By strategically placing > 0.01x SVs on decimal places beyond the High BPM line, we can create a new frame every time.

For Example, assume Empty repeats 1 time, and we have 9 functions.::

    +            [0] [1] [2] [3][3.1][3.2][...][3.9][4] | [5] [6] [7] [8][8.1][8.2][...][8.9][9] | ...
    S{_}...D{F} = S           D   F1   F2        F9     |  S           D   F1   F2        F9     | ...
                 |||         |||  +---------------+       |||         |||  +---------------+
                STOP      DEPENDENT   FUNCTIONS          STOP      DEPENDENT   FUNCTIONS

How does it bypass the 1ms rule? It actually doesn't use BPM Lines during the 3.1 ~ 3.9 section.

Dependent
=========

The dependent Bpm is calculated by :math:`dep_{bpm} = 60000 * (len(funcs) + 1)`. We do this because we don't need to
generate the maximum possible measure lines every time.

Having a low :math:`dep_{bpm}` helps in map loading times.

Algorithm Optimizations
=======================

- The algorithm is optimized to reduce the highest BPM required by counting the amount of functions required to be
    generated.
- The algorithm takes into account clashing lines, that is, if you have 2 lines that require a ``< MIN_SV`` distance,
    it will not affect the other functions.

FYI: Maximum Measure Line Count
===============================

The number of measure lines generated on 1/1 metronome is dependent on the reference Bpm.
This is the maximum possible measure lines

.. math::

    measureLines_{max}(bpm_{ref}) = 100 * SDF * bpm_{ref} / (60 * 1,000)

Hence if the reference Bpm is higher, there will be more measure lines to work with.

.. math::

    \begin{align*}
        & measureLines_{max}(200) = 100 * SDF * 200 / (60 * 1000) \approx 166 \\
        & measureLines_{max}(400) = 100 * SDF * 400 / (60 * 1000) \approx 333 \\
        & measureLines_{max}(800) = 100 * SDF * 400 / (60 * 1000) \approx 666 \\
    \end{align*}

Anything higher will indeed create more measure lines, however they will be of the same density.
e.g. 200 SDF will create double measure lines, but they span 2 screen's length.

Spanning 2 ms
-------------

We could use 50 SDF to span 2 milliseconds, however there's a non-negligible chance that there's a flicker when
the second ms renders.

This could be interesting to research.
