######
MapSet
######

********
Describe
********

Map sets will loop through describe.

.. code-block:: python
    :linenos:

    from reamber.algorithms.analysis.describe.describe import describe

    s = SMMapSet.readFile("path/to/file.sm")
    describe(m=s.maps[0], s=s)

.. code-block::
    :linenos:

    Average BPM: 175.0
    Map Length: 0:06:48.514000
    Camellia - I Can Fly In The Universe, Schizophrenia (Evening)
    ---- NPS ----
    hits
    Count: 6036, 50% (Median): 12.00, 75%: 14.00, 100% (Max): 24.00
    holds
    Count: 860, 50% (Median): 9.00, 75%: 12.00, 100% (Max): 12.00
    Average BPM: 172.0

****
Rate
****

Acts like a rate changer. Note that this applies to all difficulties.

**Input**

.. code-block:: python
   :linenos:

    s = SMMapSet.readFile("path/to/file.sm")
    s.rate(2.0, inplace=True)
    s.writeFile("path/to/file200.sm")

***********
Module Info
***********

.. automodule:: reamber.base.MapSet