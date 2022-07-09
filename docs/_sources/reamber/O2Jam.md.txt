# O2Jam

**OJM is not supported, hence the following will not be supported.**

- Writing to O2Jam (OJN, OJM)
- Reading OJN
- Reading the Music File
- Exporting to MP3
- Exporting to Keysounds

## Examples

Not many examples since this is not writable.

### Read

Writing is not supported. However, you can convert it to other formats.

```python
from reamber.o2jam.O2JMapSet import O2JMapSet
o2js = O2JMapSet.read_file("file.ojn")
```

### Get the number of Hits of the Easy Map

```python
from reamber.o2jam.O2JMapSet import O2JMapSet

o2js = O2JMapSet.read_file("file.ojn")
print(len(o2js[0].hits))
```