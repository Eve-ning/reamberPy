_HEADER = {
        # Will support these if there's demand
        # b'01':"SAMPLE",
        # b'02':"TIME_SIG",
        b'03':"BPM_CHANGE",
        # b'09':"STOP" Will not support stops for now unless there's a large demand
    }
class BMSChannel:

    BMS = {**_HEADER,
        b'11': 0, b'21': 7,
        b'12': 1, b'22': 8,
        b'13': 2, b'23': 9,
        b'14': 3, b'24': 10,
        b'15': 4, b'25': 11,
        b'16': 5, b'26': 12,
        b'17': 6, b'27': 13}
    BME = {**_HEADER,
        b'16': 0, b'21': 7,
        b'11': 1, b'22': 8,
        b'12': 2, b'23': 9,
        b'13': 3, b'24': 10,
        b'14': 4, b'25': 11,
        b'15': 5, b'28': 12,
        b'18': 6, b'29': 13,
        b'19': 7, b'26': 14}
    PMS = {**_HEADER,
        b'11': 0,
        b'12': 1,
        b'13': 2,
        b'14': 3,
        b'15': 4,
        b'22': 5,
        b'23': 6,
        b'24': 7,
        b'25': 8}
    PMS_BME = {**_HEADER,
        b'11': 0, b'21': 9,
        b'12': 1, b'22': 10,
        b'13': 2, b'23': 11,
        b'14': 3, b'24': 12,
        b'15': 4, b'25': 13,
        b'18': 5, b'28': 14,
        b'19': 6, b'29': 15,
        b'16': 7, b'26': 16,
        b'17': 8, b'27': 17}
