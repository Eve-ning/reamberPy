SV Osu Measure Lines Info
=========================

Acknowledgements
----------------

Inspired by datoujia's method.

Intro
-----

Knowledge of Algo 1 and 2 aren't required but good to have

Screen Distance Factor (SDF)
----------------------------

*If your reference bpm is 200, and the current is 400, you'd see the scroll move twice as fast.*

As an estimation, 100,000 Bpm for 1 ms will travel the screen's length if the reference bpm is around 200.

Hence the **(SDF) Screen Distance Factor** is around 4,800 ~ 5,000. For calculation, we'll use 5,000.

**SDF** is independent of the reference BPM, that's why we'll refer to this.

**100 SDF** for 1ms on 0.01x Sv will travel the screen's length.

**For simplicity, all SDFs are assumed to be on 0.01x SV**

Measure Line Count
------------------

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

50 SDF ?
^^^^^^^^

We could use 50 SDF to span 2 milliseconds, however there's a non-negligible chance that there's a flicker when
the second ms renders.

This could be interesting to research.

Cons
----

- One of the biggest limitations is that the distance of lines cannot be smaller than the distance measured at 0.01x SV.
    This is because you cannot have < 0.01x SV.

Pros
----

- This doesn't have to deal with a lot of weird BPM nuances like in Algo 1 and 2.
- This has virtually no flickering.
- This algorithm is easier to set up.


