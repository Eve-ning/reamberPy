# MapSet

## Describe

Map sets will loop through describe.

```python
from reamber.sm.SMMapSet import SMMapSet

sm = SMMapSet.read_file(".scratch/Escapes.sm")
d = (sm.describe(unicode=False))
```

```
Average BPM: 155.45
Map Length: 0:02:45.202577
Draw the Emotional x Foreground Eclipse - Escapes, Hard ()
--- Notes ---

...

SMHitList
Index(['offset', 'column'], dtype='object')
              offset       column
count    1816.000000  1816.000000
mean    81022.787207     1.502203
std     46502.778494     1.077184
min      -635.000000     0.000000
25%     36270.172414     1.000000
50%     83985.689655     2.000000
75%    123103.291019     2.000000
max    161653.291019     3.000000
SMHoldList
Index(['offset', 'column', 'length'], dtype='object')
              offset     column       length
count      47.000000  47.000000    47.000000
mean    54359.206381   1.659574   440.771408
std     25807.318705   1.166127   537.370286
min      -635.000000   0.000000    25.862069
25%     45606.379310   1.000000    64.655172
50%     49847.758621   2.000000   413.793103
75%     61640.862069   3.000000   413.793103
max    163196.148162   3.000000  3310.344828
```

## Rate

Acts like a rate changer. Note that this applies to all difficulties.

**Input**

```python
from reamber.sm.SMMapSet import SMMapSet
s = SMMapSet.read_file("path/to/file.sm")
s_ = s.rate(2.0)
s_.write_file("path/to/file200.sm")
```
