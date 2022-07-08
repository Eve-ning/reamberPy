# Quaver

## Examples

### Read and Write

```python
from reamber.quaver.QuaMap import QuaMap

q = QuaMap.read_file("file.qua")
q.write_file("file_out.qua")
```

### Prints all the SV Multipliers

```python
from reamber.quaver.QuaMap import QuaMap

q = QuaMap.read_file("file.qua")

print(q.svs.multiplier)
```

### Multiply all Bpms and Svs by 1.5

```python
from reamber.quaver.QuaMap import QuaMap

q = QuaMap.read_file("file.qua")

q.svs.multiplier *= 1.5
q.bpms.bpm *= 1.5
```