import pandas as pd
from typing import List


def rollingDensity(offsets: List[float], rollingWindowS: float = None) -> pd.Series:
    """ Returns the Density DF for any list
    :param offsets: Any List of offsets
    :param rollingWindowS: The window to search in seconds. If left as None, the window is 0
    :return: Col 0 Offset (DateTime), Col 1 Density (Int)
    """
    df = pd.DataFrame({'offset': offsets})
    df['count'] = 1
    df['offset'] = pd.to_timedelta(df['offset'], unit='ms')
    df = df.groupby('offset').sum()
    if rollingWindowS is not None:
        df = df.rolling(f"{rollingWindowS}s").count()
        df['count'] /= rollingWindowS
        return df.iloc[:, 0]
    else:
        return df.iloc[:, 0]
