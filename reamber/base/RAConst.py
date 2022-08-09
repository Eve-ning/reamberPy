class RAConst:
    """This class holds all constants that can be used throughout the program

    The class defines a helper classes to convert in units

    Examples:

        >>> RAConst.hr_to_min(10)
        600.0

        >>> RAConst.min_to_sec(10)
        600.0

        >>> RAConst.sec_to_msec(10)
        10000.0

        >>> RAConst.sec_to_hr(60 * 60)
        1.0

    Notes:
        This also defines division classes, used in PlayField::

             {1: "#969696",
              2: "#b02323",
              3: "#8a23b0",
              4: "#2399b0",
              5: "#ffdfbd",
              6: "#b02378",
              8: "#b06c23",
              12: "#23b09d",
              16: "#3db023",
              24: "#94b023",
              32: "#23b052"}

    """

    HR_TO_MIN   : float = 60.0
    HR_TO_SEC   : float = 60.0 * 60.0
    HR_TO_MSEC  : float = 60.0 * 60.0 * 1000.0
    MIN_TO_HR   : float = 1.0 / 60.0
    MIN_TO_SEC  : float = 60.0
    MIN_TO_MSEC : float = 60.0 * 1000.0
    SEC_TO_HR   : float = 1.0 / (60.0 * 60.0)
    SEC_TO_MIN  : float = 1.0 / 60.0
    SEC_TO_MSEC : float = 1000.0
    MSEC_TO_HR  : float = 1.0 / (60.0 * 60.0 * 1000.0)
    MSEC_TO_MIN : float = 1.0 / (60.0 * 1000.0)
    MSEC_TO_SEC : float = 1.0 / 1000.0

    @staticmethod
    def hr_to_min(hours): return float(hours * RAConst.HR_TO_MIN)
    @staticmethod
    def hr_to_sec(hours): return float(hours * RAConst.HR_TO_SEC)
    @staticmethod
    def hr_to_msec(hours): return float(hours * RAConst.HR_TO_MSEC)
    @staticmethod
    def min_to_hr(mins): return float(mins * RAConst.MIN_TO_HR)
    @staticmethod
    def min_to_sec(mins): return float(mins * RAConst.MIN_TO_SEC)
    @staticmethod
    def min_to_msec(mins): return float(mins * RAConst.MIN_TO_MSEC)
    @staticmethod
    def sec_to_hr(secs): return float(secs * RAConst.SEC_TO_HR)
    @staticmethod
    def sec_to_min(secs): return float(secs * RAConst.SEC_TO_MIN)
    @staticmethod
    def sec_to_msec(secs): return float(secs * RAConst.SEC_TO_MSEC)
    @staticmethod
    def msec_to_hr(msecs): return float(msecs * RAConst.MSEC_TO_HR)
    @staticmethod
    def msec_to_min(msecs): return float(msecs * RAConst.MSEC_TO_MIN)
    @staticmethod
    def msec_to_sec(msecs): return float(msecs * RAConst.MSEC_TO_SEC)

    # These are the colors to indicate snapping. Used for PlayField
    DIVISION_COLORS = {1: "#969696"
                     , 2: "#b02323"
                     , 3: "#8a23b0"
                     , 4: "#2399b0"
                     , 5: "#ffdfbd"
                     , 6: "#b02378"
                     , 8: "#b06c23"
                     , 12: "#23b09d"
                     , 16: "#3db023"
                     , 24: "#94b023"
                     , 32: "#23b052"}
