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

There are multiple methods available in ``reamber.base.RAConst`` for conversion
::

    # All are static
    def hr_to_min(hours):   return float(hours * RAConst.HR_TO_MIN)
    def hr_to_sec(hours):   return float(hours * RAConst.HR_TO_SEC)
    def hr_to_msec(hours):  return float(hours * RAConst.HR_TO_MSEC)
    def min_to_hr(mins):    return float(mins * RAConst.MIN_TO_HR)
    def min_to_sec(mins):   return float(mins * RAConst.MIN_TO_SEC)
    def min_to_msec(mins):  return float(mins * RAConst.MIN_TO_MSEC)
    def sec_to_hr(secs):    return float(secs * RAConst.SEC_TO_HR)
    def sec_to_min(secs):   return float(secs * RAConst.SEC_TO_MIN)
    def sec_to_msec(secs):  return float(secs * RAConst.SEC_TO_MSEC)
    def msec_to_hr(msecs):  return float(msecs * RAConst.MSEC_TO_HR)
    def msec_to_min(msecs): return float(msecs * RAConst.MSEC_TO_MIN)
    def msec_to_sec(msecs): return float(msecs * RAConst.MSEC_TO_SEC)

**Map & MapSet**

A MapSet contains Maps.

**Notes**

``Note`` s can be either a ``Hit`` or ``Hold``.

``Note`` is the parent of those two.

This naming convention is used because it's easier to differentiate.

**BPM Points**

Think this is pretty obvious, I don't use ``TimingPoint`` because it's confusing.

