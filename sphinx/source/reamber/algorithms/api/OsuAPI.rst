#######
Osu API
#######

There are 2 versions, currently, V1 is more supported because V2 is very volatile.

All necessary information about the API can be found here. `osu! API Wiki <https://github.com/ppy/osu-api/wiki>`_

=======
Example
=======

How to set up the ini/cfg file is detailed in :doc:`API <../api>`

.. code-block:: python

    from reamber.algorithms.api.osu.OsuAPIV1 import OsuAPIV1
    import json

    api = OsuAPIV1.from_cfg(cfg_path="api.ini")

    req = api.get_beatmaps(m=3, since="2020-08-01")
    content = json.loads(req.content)
    print(content)

***********
Module Info
***********

==
V1
==

.. automodule:: reamber.algorithms.api.osu.OsuAPIV1

==
V2
==

**Not fully supported**

.. automodule:: reamber.algorithms.api.osu.OsuAPIV2