_HEADER = {
        # Will support these if there's demand
        # b'01':"SAMPLE",
        2: "TIME_SIG",
        3: "BPM_CHANGE",
        # b'09':"STOP" Will not support stops for now unless there's a large demand
    }
class BMSChannel:

    TIME_SIG = 2
    BPM_CHANGE = 3

    BMS = {**_HEADER,
        11: 0, 21: 7,
        12: 1, 22: 8,
        13: 2, 23: 9,
        14: 3, 24: 10,
        15: 4, 25: 11,
        16: 5, 26: 12,
        17: 6, 27: 13}
    BME = {**_HEADER,
        16: 0, 21: 8,
        11: 1, 22: 9,
        12: 2, 23: 10,
        13: 3, 24: 11,
        14: 4, 25: 12,
        15: 5, 28: 13,
        18: 6, 29: 14,
        19: 7, 26: 15}
    PMS = {**_HEADER,
        11: 0,
        12: 1,
        13: 2,
        14: 3,
        15: 4,
        22: 5,
        23: 6,
        24: 7,
        25: 8}
    PMS_BME = {**_HEADER,
        11: 0, 21: 9,
        12: 1, 22: 10,
        13: 2, 23: 11,
        14: 3, 24: 12,
        15: 4, 25: 13,
        18: 5, 28: 14,
        19: 6, 29: 15,
        16: 7, 26: 16,
        17: 8, 27: 17}
    PMS_5B = {**_HEADER,
        13: 0,
        14: 1,
        15: 2,
        22: 3,
        23: 4}
