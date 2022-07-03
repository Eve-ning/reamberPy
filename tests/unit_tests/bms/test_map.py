from pathlib import Path

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import PFDrawBeatLines, PFDrawNotes, \
    PFDrawBpm

THIS_DIR = Path(__file__).parent

MAP_READ = THIS_DIR / 'searoad.bml'
MAP_WRITE_EXP = THIS_DIR / 'map_write_expected.bme'
MAP_WRITE = THIS_DIR / 'map_write.bme'


def test_describe(bms_map):
    bms_map.describe()


def test_meta(bms_map):
    assert bms_map.title == b'searoad tracks =side blue= (LN-Applied)'
    assert bms_map.artist == b'sasakure.UK / obj:moya'
    assert bms_map.version == b'16'


def test_draw(bms_map):
    bms_map.write_file(MAP_WRITE)
    pf = PlayField(bms_map.read_file(MAP_WRITE), padding=50) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=2300).save("sm.png")
