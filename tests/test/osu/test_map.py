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

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_READ = os.path.join(THIS_DIR, 'map_read.osu')
MAP_WRITE_EXP = os.path.join(THIS_DIR, 'map_write_expected.osu')
MAP_WRITE = os.path.join(THIS_DIR, 'map_write.osu')


class TestOsuMap(unittest.TestCase):

    def setUp(self) -> None:
        self.map = OsuMap.read_file(MAP_READ)

    def test_read_bad(self):
        with self.assertRaises(Exception):
            OsuMap.read(["bad_string"])
        with self.assertRaises(Exception):
            OsuMap.read([])

    def test_types(self):
        self.assertIsInstance(self.map.hits, OsuHitList)
        self.assertIsInstance(self.map.holds, OsuHoldList)
        self.assertIsInstance(self.map.svs, OsuSvList)
        self.assertIsInstance(self.map.bpms, OsuBpmList)
        self.assertIsInstance(self.map.objects, list)

    def test_write(self):
        self.map.write_file(MAP_WRITE)
        with open(MAP_WRITE_EXP) as f:
            expected = f.read()
        with open(MAP_WRITE) as f:
            actual = f.read()
        self.assertEqual(expected, actual)

    def test_meta(self):
        self.assertEqual("audio.mp3", self.map.audio_file_name)  # : str = ""
        self.assertEqual(0, self.map.audio_lead_in)  # : int = 0
        self.assertEqual(86398, self.map.preview_time)  # : int = -1
        self.assertEqual(False, self.map.countdown)  # : bool = False
        self.assertEqual(Sample.SOFT, self.map.sample_set)  # : int = OsuSampleSet.AUTO
        self.assertEqual(0.7, self.map.stack_leniency)  # : float = 0.7
        self.assertEqual(OsuMapMode.MANIA, self.map.mode)  # : int = OsuMapMode.MANIA
        self.assertEqual(False, self.map.letterbox_in_breaks)  # : bool = False
        self.assertEqual(False, self.map.special_style)  # : bool = False
        self.assertEqual(True, self.map.widescreen_storyboard)  # : bool = True
        self.assertEqual(0.4, self.map.distance_spacing)  # : float = 4
        self.assertEqual(8, self.map.beat_divisor)  # : int = 4
        self.assertEqual(4, self.map.grid_size)  # : int = 8
        self.assertEqual(1.9, self.map.timeline_zoom)  # : float = 0.3
        self.assertEqual("Tribal Trial", self.map.title)  # : str = ""
        self.assertEqual("Tribal Trial", self.map.title_unicode)  # : str = ""
        self.assertEqual("Yooh", self.map.artist)  # : str = ""
        self.assertEqual("Yooh", self.map.artist_unicode)  # : str = ""
        self.assertEqual("Tofu1222", self.map.creator)  # : str = ""
        self.assertEqual("Murumoo's EXHAUST", self.map.version)  # : str = ""
        self.assertEqual("SOUND VOLTEX VIVID WAVE", self.map.source)  # : str = ""
        self.assertEqual(["BEMANI", "KONAMI", "SDVX", "V", "5", "Murumoo",
                          "Unpredictable", "FAMoss", "Video", "Game", "Instrumental"], self.map.tags)  # : List[str] = ""
        self.assertEqual(2062527, self.map.beatmap_id)  # : int = 0
        self.assertEqual(965664, self.map.beatmap_set_id)  # : int = -1
        self.assertEqual(7.5, self.map.hp_drain_rate)  # : float = 5.0
        self.assertEqual(4, self.map.circle_size)  # : float = 4.0
        self.assertEqual(7.5, self.map.overall_difficulty)  # : float = 5.0
        self.assertEqual(5, self.map.approach_rate)  # : float = 5.0
        self.assertEqual(1.4, self.map.slider_multiplier)  # : float = 1.4
        self.assertEqual(1, self.map.slider_tick_rate)  # : int = 1
        self.assertEqual("BG.png", self.map.background_file_name)

    def test_sample(self):
        # noinspection PyTypeChecker
        self.assertTrue(all(OsuSampleList([OsuSample(24565, "clap.wav", 70)]).df.sort_index(axis=1)
                            == self.map.samples.df.sort_index(axis=1)))

    def test_deepcopy(self):
        m = self.map.deepcopy()
        self.assertIsNot(m, self.map)
        self.assertIsInstance(m, OsuMap)

    def test_svs(self):
        self.assertIsInstance(self.map.svs, OsuSvList)

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
