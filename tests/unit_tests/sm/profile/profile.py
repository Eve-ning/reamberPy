from line_profiler_pycharm import profile

from reamber.sm.SMMapSet import SMMapSet
from tests.conftest import MAPS_DIR

MAP_PATH = MAPS_DIR / "sm/caravan"


@profile
def main():
    ms = SMMapSet.read_file(MAP_PATH)
    ms.write()


if __name__ == '__main__':
    main()
