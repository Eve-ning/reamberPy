class OsuSampleSet:
    """ Osu SampleSet are a "enum" of available hitsounds.

    Not to be confused with OsuSample, where that's a class for samples under [Events]
    """
    AUTO: int = 0
    NORMAL: int = 1
    SOFT: int = 2
    DRUM: int = 3

    @staticmethod
    def toString(sampleSet: int) -> str:
        """ Converts a integer to a string representing SampleSet """
        if sampleSet == OsuSampleSet.AUTO:
            return "None"
        elif sampleSet == OsuSampleSet.NORMAL:
            return "Normal"
        elif sampleSet == OsuSampleSet.SOFT:
            return "Soft"
        elif sampleSet == OsuSampleSet.DRUM:
            return "Drum"
        else:
            return "Invalid"

    @staticmethod
    def fromString(sampleSet: str) -> int:
        """ Converts a string to an integer """
        if sampleSet == "None":
            return OsuSampleSet.AUTO
        elif sampleSet == "Normal":
            return OsuSampleSet.NORMAL
        elif sampleSet == "Soft":
            return OsuSampleSet.SOFT
        elif sampleSet == "Drum":
            return OsuSampleSet.DRUM
        else:
            return -1
