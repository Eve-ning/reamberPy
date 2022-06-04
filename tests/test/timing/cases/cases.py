from reamber.algorithms.timing.utils.snap import Snap
from tests.test.timing.cases.case import Case, BpmChange

C = 60000

case_reseat_0 = Case([
    BpmChange(C / 100, 4, 0, Snap(0, 0, 4), Snap(0, 0, 4), C / 50),
    BpmChange(C / 100, 4, 200, Snap(0, 2, 4), Snap(1, 0, 4), C / 100),
    BpmChange(C / 100, 4, 600, Snap(1, 2, 4), Snap(2, 0, 4), C / 100)
])

case_reseat_1 = Case([
    BpmChange(C / 100, 4, 0, Snap(0, 0, 4), Snap(0, 0, 4), C / 50),
    BpmChange(C / 100, 4, 200, Snap(0, 2, 4), Snap(1, 0, 4), C / 100),
    BpmChange(C / 100, 4, 600, Snap(1, 2, 4), Snap(2, 0, 4), C / 100)
])
