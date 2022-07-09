from reamber.algorithms.timing.utils.snap import Snap
from tests.unit_tests.timing.cases.case import Case, BpmChange

C = 60000

cases = dict(
    case_reseat_4_4=Case([
        BpmChange(100, 4, 0, Snap(0, 0, 4), Snap(0, 0, 4), 100),
        BpmChange(100, 4, 400, Snap(1, 0, 4), Snap(1, 0, 4), 100),
    ]),
    case_reseat_2_4=Case([
        BpmChange(100, 4, 0, Snap(0, 0, 4), Snap(0, 0, 4), 50),
        BpmChange(100, 4, 200, Snap(0, 2, 4), Snap(1, 0, 4), 100),
    ]),
    case_reseat_05_4=Case([
        BpmChange(100, 4, 0, Snap(0, 0, 4), Snap(0, 0, 4), 100 / 8),
        BpmChange(100, 4, 50, Snap(0, 0.5, 4), Snap(1, 0, 4), 100),
    ]),
    case_reseat_1_1_4=Case([
        BpmChange(100, 4, 0, Snap(0, 0, 4), Snap(0, 0, 4), 100 / 4),
        BpmChange(100, 4, 100, Snap(0, 1, 4), Snap(1, 0, 4), 100 / 4),
        BpmChange(100, 4, 200, Snap(0, 2, 4), Snap(2, 0, 4), 100),
    ]),
    case_reseat_approx=Case([
        BpmChange(100, 4, 0, Snap(0, 0, 4), Snap(0, 0, 4), 100 / 4),
        BpmChange(100, 4, 100.0001, Snap(0, 1, 4), Snap(1, 0, 4), 100),
    ]),
    case_reseat_neg=Case([
        BpmChange(100, 4, -100, Snap(0, 0, 4), Snap(0, 0, 4), 100 / 4),
        BpmChange(100, 4, 0, Snap(0, 1, 4), Snap(1, 0, 4), 100),
    ])
)
