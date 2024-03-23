# BMS

There are few features excluded intentionally:

- Sample Loading
- Sample Writing (That means you can only write notes, you'd have to
  insert the song/samples manually)
- BGA
- Mines

## Examples

### Read and Write

> There are multiple [**channel configurations**](Channel.md) for BMS maps
> If you're unsure reference the file extension.
> In this case we have `.bme` thus we use `BMSChannel.BME`.

```python
from reamber.bms.BMSMap import BMSMap
from reamber.bms.BMSChannel import BMSChannel

bms = BMSMap.read_file("file.bme", note_channel_config=BMSChannel.BME)
bms.write_file("file_out.bme")
```

### Prints all the BPMs

```python
from reamber.bms.BMSMap import BMSMap

bms = BMSMap.read_file("path/to/file.bme")
print(bms.bpms.bpm)
```

### Move all columns to the right by 1

```python
from reamber.bms.BMSMap import BMSMap

bms = BMSMap.read_file("path/to/file.bme")

bms.hits.column += 1
bms.holds.column += 1
```
