################
SV Normalize Bpm
################

Let's say we have the following::

    OFFSET BPM
    0      200
    100    50
    300    100

If the game decides that it's reference BPM is 100; that is, it shows normal scroll speed during 100 BPM Sections.

Then you would call the algorithm as such

.. code-block:: python
   :linenos:

    # Assume osu is the map itself
    seq = sv_normalize_bpm(osu.bpm, 100)
    svs = seq.write_as_sv(OsuSv)

`svs` would be the output.

.. automodule:: reamber.algorithms.generate.sv.generators.sv_normalize_bpm