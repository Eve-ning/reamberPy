Conventions
===========

**Units**

Unless specifically specified. The units used for the package are

+---------+------------------+
| Unit of | Unit as          |
+=========+==================+
| Time    | Milliseconds     |
+---------+------------------+
| BPM     | Beats Per Minute |
+---------+------------------+
| Column  | Integer from 0   |
+---------+------------------+

There are multiple methods available in `reamber.base.RAConst` for conversion
::

    # All are static
    def hrToMin(hours):   return float(hours * RAConst.HR_TO_MIN)
    def hrToSec(hours):   return float(hours * RAConst.HR_TO_SEC)
    def hrToMSec(hours):  return float(hours * RAConst.HR_TO_MSEC)
    def minToHr(mins):    return float(mins * RAConst.MIN_TO_HR)
    def minToSec(mins):   return float(mins * RAConst.MIN_TO_SEC)
    def minToMSec(mins):  return float(mins * RAConst.MIN_TO_MSEC)
    def secToHr(secs):    return float(secs * RAConst.SEC_TO_HR)
    def secToMin(secs):   return float(secs * RAConst.SEC_TO_MIN)
    def secToMSec(secs):  return float(secs * RAConst.SEC_TO_MSEC)
    def mSecToHr(msecs):  return float(msecs * RAConst.MSEC_TO_HR)
    def mSecToMin(msecs): return float(msecs * RAConst.MSEC_TO_MIN)
    def mSecToSec(msecs): return float(msecs * RAConst.MSEC_TO_SEC)

**Map & MapSet**

A MapSet contains Maps.

**Notes**

`NoteObject`s can be either a `HitObject` or `HoldObject`.

`NoteObject` is the parent of those two.

This naming convention is used because it's easier to differentiate.

**BPM Points**

Think this is pretty obvious, I don't use `TimingPoint` because it's confusing.

