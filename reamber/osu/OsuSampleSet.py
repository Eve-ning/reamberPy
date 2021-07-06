class OsuSampleSet:
    """ Osu SampleSet are a "enum" of available hitsounds.

    Not to be confused with OsuSample, where that's a class for samples under [Events]
    """
    AUTO: int = 0
    NORMAL: int = 1
    SOFT: int = 2
    DRUM: int = 3

    @staticmethod
    def to_string(sample_set: int) -> str:
        """ Converts a integer to a string representing SampleSet """
        if sample_set == OsuSampleSet.AUTO:
            return "None"
        elif sample_set == OsuSampleSet.NORMAL:
            return "Normal"
        elif sample_set == OsuSampleSet.SOFT:
            return "Soft"
        elif sample_set == OsuSampleSet.DRUM:
            return "Drum"
        else:
            return "Invalid"

    @staticmethod
    def from_string(sample_set: str) -> int:
        """ Converts a string to an integer """
        if sample_set == "None":
            return OsuSampleSet.AUTO
        elif sample_set == "Normal":
            return OsuSampleSet.NORMAL
        elif sample_set == "Soft":
            return OsuSampleSet.SOFT
        elif sample_set == "Drum":
            return OsuSampleSet.DRUM
        else:
            return -1
