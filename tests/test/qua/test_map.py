import os
import unittest

from reamber.osu import OsuBpm, OsuSampleSet as Sample, OsuMap
from reamber.osu.OsuMapMeta import OsuMapMode
from reamber.osu.OsuSample import OsuSample
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuSampleList import OsuSampleList
from reamber.osu.lists.OsuSvList import OsuSvList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.quaver.QuaMapMeta import QuaMapMode

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_WRITE_EXP = os.path.join(THIS_DIR, 'map_write_expected.qua')
MAP_WRITE = os.path.join(THIS_DIR, 'map_write.qua')
import pandas as pd

from reamber.quaver import QuaHit, QuaMap
from tests.test.qua.test_fixture import qua_map

def test_type(qua_map):
    assert isinstance(qua_map, QuaMap)

def test_meta(qua_map):
    assert qua_map.audio_file           == "audio.mp3"
    assert qua_map.song_preview_time    == 169955
    assert qua_map.background_file      == "bg.jpg"
    assert qua_map.map_id               == -1
    assert qua_map.map_set_id           == -1
    assert qua_map.mode                 == QuaMapMode.KEYS_7
    assert qua_map.title                == "Carry Me Away (Extended Mix)"
    assert qua_map.artist               == "lapix"
    assert qua_map.source               == ''
    assert qua_map.tags                 == []
    assert qua_map.creator              == "Evening"
    assert qua_map.difficulty_name      == "Airbound (Evening's Flip)"
    assert qua_map.description          == "This is a Quaver converted version of Evening's map."
    assert qua_map.editor_layers        == []
    assert qua_map.custom_audio_samples == []
    assert qua_map.sound_effects        == []

def test_deepcopy(qua_map):
    assert qua_map.deepcopy() is not qua_map

def test_write(qua_map):
    qua_map.write_file(MAP_WRITE)
    with open(MAP_WRITE_EXP) as f:
        expected = f.read()
    with open(MAP_WRITE) as f:
        actual = f.read()
    assert expected == actual

def test_stack_mutate(self):
    self.map.stack.volume        += 1
    self.map.stack.custom_set    += 1
    self.map.stack.sample_set    += 1
    self.map.stack.hitsound_set  += 1
    self.map.stack.addition_set  += 1
    self.map.stack.hitsound_file += "_"
    self.map.stack.sample_set_index += 1
    self.map.stack.kiai |= True

    with self.assertRaises(TypeError): self.map.stack.volume += "_"
    with self.assertRaises(TypeError): self.map.stack.custom_set += "_"
    with self.assertRaises(TypeError): self.map.stack.sample_set += "_"
    with self.assertRaises(TypeError): self.map.stack.hitsound_set += "_"
    with self.assertRaises(TypeError): self.map.stack.addition_set += "_"
    with self.assertRaises(TypeError): self.map.stack.hitsound_file += 1
    with self.assertRaises(TypeError): self.map.stack.sample_set_index += "_"
    with self.assertRaises(TypeError): self.map.stack.kiai += "_"


if __name__ == '__main__':
    unittest.main()
