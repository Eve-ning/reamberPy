Scroll Velocities
=================

**Not supported beyond v0.1.0, open to request of revival.**

*alias: slider velocity*

Scroll Velocities are mainly relevant in osu! and Quaver.

However, you can also export them as BPM Lines in all types to mimic SVs with `write_as_bpm`

.. toctree::
   :maxdepth: 1

    Osu Measure Line <sv/generators/SvOsuMeasureLine>
    Normalize Bpm <sv/generators/SvNormalizeBpm>
    Function Sequencer <sv/generators/SvFuncSequencer>

Sequences and Packages
----------------------

The main difference between the SV Package and SV Sequence is that a package holds multiple SV Sequences.

The purpose of a sequence is to hold **single sv patterns**, those that you expect to **repeat**.

The purpose of a package is to hold **multiple sv patterns**, those that you expect to **combine**.

A **combined** package is a sequence, rinse and repeat if needed.

Each of these classes have dedicated helper methods to improve your workflow.

The following is an example that uses both the sequence and package.

.. code-block:: python
   :linenos:

    from reamber.algorithms.generate.sv.SvSequence import SvSequence
    from reamber.algorithms.generate.sv.SvPkg import SvPkg

    seq = SvSequence([0, (100, 1.5, True), 200])
    # OFFSET SV    FIXED
    # 0      1.0   False
    # 100    1.5   True
    # 200    1.0   False

    seq.normalize_to(aveSv=1.0, inplace=True)
    # OFFSET SV    FIXED
    # 0      0.5   False
    # 100    1.5   True  ! Fixed means normalized will attempt to not
    # 200    1.0   False   change it to fit the aveSv

    seqPkg = SvPkg.repeat(seq, 3)
    # OFFSET SV  | OFFSET SV  | OFFSET SV
    # 0      0.5 | 200    0.5 | 400    0.5
    # 100    1.5 | 300    1.5 | 500    1.5
    # 200    1.0 | 400    1.0 | 600    1.0

    seqCombine = seqPkg.combine(SvPkg.CombineMethod.DROP_BY_POINT)
    # OFFSET SV
    # 0      0.5 ! Combine by point means it will drop any repeating Svs.
    # 100    1.5   Priority defaults to the later ones.
    # 200    0.5
    # 300    1.5
    # 400    0.5
    # 500    1.5
    # 600    1.0

Take note on what functions gives you a package, and what functions gives you a sequence.

Sequence
--------

.. automodule:: reamber.algorithms.generate.sv.SvSequence

Package
-------

.. automodule:: reamber.algorithms.generate.sv.SvPkg

