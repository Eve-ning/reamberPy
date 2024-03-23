# SV Normalize

<tldr>
    <p>Generates SVs that normalizes the scroll speed of the map.</p>
</tldr>

> This only creates the SV List, and doesn't append to the map. 

## Usage

Find the normalizing SVs of a map

<tabs>
    <tab title="osu!mania">
        <code-block lang="python">
        from reamber.algorithms.generate import sv_normalize
        from reamber.osu import OsuMap
        from reamber.osu.lists import OsuSvList&#xA;
        osu_map = OsuMap.read_file(...)
        svs = sv_normalize(osu_map)&#xA;
        # Append new svs to our map
        osu_map.svs = osu_map.svs.append(svs)&#xA;
        # Remove any duplicates, if any
        # This is because the SVs generated may overlap with existing SVs
        osu_map.svs = OsuSvList(osu_map.svs.df.drop_duplicates())
        </code-block>
    </tab>
    <tab title="Quaver">
        <code-block lang="python">
        from reamber.algorithms.generate import sv_normalize
        from reamber.qua import QuaMap
        from reamber.qua.lists import QuaSvList&#xA;
        qua_map = QuaMap.read_file(...)
        svs = sv_normalize(qua_map)&#xA;
        # Append new svs to our map
        qua_map.svs = qua_map.svs.append(svs)&#xA;
        # Remove any duplicates, if any
        # This is because the SVs generated may overlap with existing SVs
        qua_map.svs = QuaSvList(qua_map.svs.df.drop_duplicates())
        </code-block>
    </tab>
</tabs>

### Override BPM

If it's not normalizing correctly, it's likely that the dominant bpm
is incorrectly found. If so, override the dominant bpm.

<tabs>
    <tab title="osu!mania">
        <code-block lang="python">
        from reamber.algorithms.generate import sv_normalize
        from reamber.osu import OsuMap&#xA;
        osu_map = OsuMap.read_file(...)
        svs = sv_normalize(osu_map, override_bpm=200)
        </code-block>        
    </tab>
    <tab title="Quaver">
        <code-block lang="python">
        from reamber.algorithms.generate import sv_normalize
        from reamber.qua import QuaMap&#xA;
        qua_map = QuaMap.read_file(...)
        svs = sv_normalize(qua_map, override_bpm=200)
        </code-block>
    </tab>
</tabs>


