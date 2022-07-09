# BMS Channel Configurations

The BMS Channel Package holds the configurations for channel handling.

That is, for different BMS Formats, ``19`` could represent ``Column 6`` or **Nothing** at all.

- Assume all **SCRATCHES** are at the ends (i.e. DP scratch is on Col 0 and 15)
- Assume all set-ups are aligned to start with 0.

| Column  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| BMS     | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 21 | 22 | 23 | 24 | 25 | 26 | 27 |    |    |    |    |
| BME     | 16 | 11 | 12 | 13 | 14 | 15 | 18 | 19 | 21 | 22 | 23 | 24 | 25 | 28 | 29 | 26 |    |    |
| PMS     | 11 | 12 | 13 | 14 | 15 | 22 | 23 | 24 | 25 |    |    |    |    |    |    |    |    |    |
| PMS_BME | 11 | 12 | 13 | 14 | 15 | 18 | 19 | 16 | 17 | 21 | 22 | 23 | 24 | 25 | 28 | 29 | 26 | 27 |
| PMS_5B  | 13 | 14 | 15 | 22 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

## Example

Consider ``#00211:01010101``.

This command states that the column code is ``11``.

In BMS, PMS, you would read it as **column 0**.

In BME, you would read it as **column 1**.

### Unsupported Formats

If you do come across a format you need to use but isn't in the package, feel free to open an issue with it, I'll add it
in promptly.

However, if you require it right now, you can create your own dictionary for ``BMSMap.read_file()`` following the format
of the dictionaries provided in ``BMSChannel``.

Note that the ``BMSChannel._HEADER`` **MUST** be included.
