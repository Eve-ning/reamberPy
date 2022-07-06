class BMSChannel:
    # The value can be 1A, 1B ... 1Z, but so far I haven't seen any?
    # If there is a need, I can change this.

    TIME_SIG = b'02'
    BPM_CHANGE = b'03'
    EXBPM_CHANGE = b'08'

    _HEADER = {
        # b'01':"SAMPLE", Sample not supported
        TIME_SIG: "TIME_SIG",
        BPM_CHANGE: "BPM_CHANGE",
        EXBPM_CHANGE: "EXBPM_CHANGE",
        # b'09':"STOP", Stops not supported
    }

    BMS = {**_HEADER,
           b'11': 0, b'21': 7,
           b'12': 1, b'22': 8,
           b'13': 2, b'23': 9,
           b'14': 3, b'24': 10,
           b'15': 4, b'25': 11,
           b'16': 5, b'26': 12,
           b'17': 6, b'27': 13}
    BME = {**_HEADER,
           b'16': 0, b'21': 8,
           b'11': 1, b'22': 9,
           b'12': 2, b'23': 10,
           b'13': 3, b'24': 11,
           b'14': 4, b'25': 12,
           b'15': 5, b'28': 13,
           b'18': 6, b'29': 14,
           b'19': 7, b'26': 15}
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
    PMS_5B = {**_HEADER,
              b'13': 0,
              b'14': 1,
              b'15': 2,
              b'22': 3,
              b'23': 4}
