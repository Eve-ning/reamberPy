SV Osu Measure Lines Info
=========================

Acknowledgements
----------------

I cannot fully list all osu!mania researchers that have put effort into discovering these methods. However, this guide
will not be possible without their contributions :)

Intro
-----

To be able to understand how measure lines are created these are the pre-requisite knowledge required.

- How a BPM affects scroll speed
- What is the *reference* bpm

Original Method
---------------

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
^^^^^^^^

If you have multiple BPM lines 1 ms after another, only the last one will render::

    OFFSET   [0][1][2][3][4][5][6][7][8][9][10]
    BPM LINE  X  X  X     X  X     X     X
    RENDERS         ^        ^     ^     ^

Stop Motion
^^^^^^^^^^^

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

Delta Distance / Framing
^^^^^^^^^^^^^^^^^^^^^^^^

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

Function
--------

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

reamberPy's Method
------------------

Sequencing
^^^^^^^^^^

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

**svOsuMeasureLine2 Algorithm**

Assume Empty repeats 2 times.
Note how Algorithm 2 flickers the functions to "fake" measure lines being rendered together::

    +            [0] [1] [2] [3] [4] [5] [6] | [7] [8] [9] [10][11][12][13]| ...
    T_S_{_}...F = T       S               F1 |  T       S               F2 | ...
                 |||     |||             |||
            TELEPORT     STOP       FUNCTION

             ... [14][15][16][17][18][19][20]| [21][22][23][24][25][26][27]|
             ...  T       S               F1 |  T       S               F2 | ...


**svOsuMeasureLine1 Algorithm**

Assume Empty repeats 1 time, and there's 2 functions.::

    +                      [0] [1] [2] [3] [4] [5] [6] [7] [8] [9] | [10][11][12][13][14][15][16][17][18][19]
    S_{_}...F{_F}..._S_T =  S           F1      F2      S       T  |  S           F1      F2      S       T

Both of these algorithms are optimized as much as possible by me. I don't doubt that there's a better way though.

SV Osu Measure Lines Annex
==========================

Here comes the complex concepts, it's not required knowledge but it may be interesting if you're creating
your own algorithm

Stop Duration
-------------
One of the concepts I haven't figured out clearly is how long each measure line should stop. It's a balancing act to
figure out how long a sequence should stop.

Consider ``svOsuMeasureLine2``, it uses ``T_S{_}...F``.

If you decrease the length of ``{_}`` to get more FPS, you'd run into the problem where there's a lot of flickering.

If you increase it, you'd run into the problem where it's too low of an FPS.

I found that ``padding`` between 5 - 30 works well. To optimize this value, it's required to calculate the length of
every frame. This tells you how long each frame lasts in milliseconds.

.. math::

    \begin{align*}
    & msecPerFrame_{algo1} = 7 + 2 * (len(funcs) - 1) + padding \\
    & msecPerFrame_{algo2} = 4 + padding
    \end{align*}

Algorithm 1
-----------

Algorithm 2 came first but I developed Algorithm 1 based on it.

The main issue I wanted to tackle is flickering of functions in Algo 1. The amount of flickering is directly
proportional to the number of ``funcs`` the algorithm accepts.

It becomes very noisy at 3 functions, and I thought of the idea of **stacking** multiple functions in a frame.

Stacking
^^^^^^^^

Here's the problem with stacking, if you stack functions together, you're adding them together.

Consider

.. math::

    \begin{align*}
    & f(x) = sin(2\pi x) + 1 \\
    & g(x) = sin(2\pi x + \pi) + 1
    \end{align*}

You'd find that these 2 functions constantly interchange locations on which should be stack on which.

What you need to do is order the results at **every x input**, sort, find the difference, then grab the correct index.

The problem is also that the user is inputting a function, so I had to create a whole new list of functions based on
those functions.

Here's the excerpt code on how I did it, it's beautiful how python let's you do this mental gymnastics.

.. code-block:: python
    :linenos:

    funcs = [lambda x: 0, *funcs]  # Add 0 offset at the start for difference calculation
    funcDiff = []

    for funcI in range(len(funcs) - 1):  # -1 due to the appended y = 0
        def f(x, i=funcI):  # i=funcI for early binding
            sort = sorted([g(x) for g in funcs])  # Sort it to get the difference
            out = [g2 - g1 for g1, g2 in zip(sort[:-1], sort[1:])][i]  # Loop through as a pair to find the difference
            if out == 0: return FALLBACK_ZERO_BPM  # Output validation
            else: return out
        funcDiff.append(deepcopy(f))  # Functions created are soft copied.

Side Effects
------------

There are many ways to make this function do weird things:

- Non-standard Teleport & Stop Bpm
- Small or Large Padding

Feel free to explore them if you're bored with standard values.

