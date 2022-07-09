# Map

## Describe

Map sets will loop through describe provided by ``pd.DataFrame``.

```py
from reamber.osu.OsuMap import OsuMap

m = OsuMap.read_file("path/to/file.osu")
print(m.describe())
```

```
Average BPM: 147.0
Map Length: 0:06:51.429000
Camellia - PLANET//SHAPER, GEOLOGICAL//IRRESOLUTION (Evening)
--- Notes ---
OsuHitList
Index(['offset', 'column', 'hitsound_set', 'sample_set', 'addition_set',
       'custom_set', 'volume', 'hitsound_file'],
      dtype='object')
              offset       column  ...  custom_set  volume
count    5108.000000  5108.000000  ...      5108.0  5108.0
mean   200896.898199     1.510376  ...         0.0     0.0
std    112978.104296     1.110363  ...         0.0     0.0
min      8639.000000     0.000000  ...         0.0     0.0
25%    102082.500000     1.000000  ...         0.0     0.0
50%    178894.000000     2.000000  ...         0.0     0.0
75%    310807.500000     2.000000  ...         0.0     0.0
max    399353.000000     3.000000  ...         0.0     0.0
[8 rows x 7 columns]
OsuHoldList
Index(['offset', 'column', 'length', 'hitsound_set', 'sample_set',
       'addition_set', 'custom_set', 'volume', 'hitsound_file'],
      dtype='object')
              offset      column       length  ...  addition_set  custom_set  volume
count     426.000000  426.000000   426.000000  ...         426.0       426.0   426.0
mean   196591.671362    1.584507   301.098592  ...           0.0         0.0     0.0
std    116253.564797    1.132886   380.376537  ...           0.0         0.0     0.0
min      2006.000000    0.000000    51.000000  ...           0.0         0.0     0.0
25%     73741.000000    1.000000   102.000000  ...           0.0         0.0     0.0
50%    232210.000000    2.000000   204.000000  ...           0.0         0.0     0.0
75%    260578.000000    3.000000   408.000000  ...           0.0         0.0     0.0
max    413027.000000    3.000000  6122.000000  ...           0.0         0.0     0.0
[8 rows x 8 columns]
```

## Metadata

```py
from reamber.osu.OsuMap import OsuMap

osu = OsuMap.read_file(".scratch/PLANETSHAPER.osu")
print(osu.metadata(unicode=False))
```

```
Camellia - PLANET//SHAPER, GEOLOGICAL//IRRESOLUTION (Evening)
```

## Rate

Acts like a rate changer

**Input**

```py
from reamber.osu.OsuMap import OsuMap

m = OsuMap.read_file("path/to/file.osu")
m_ = m.rate(2.0)
m_.write_file("path/to/file200.osu")
```
