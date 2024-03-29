import pandas as pd


def _sma(data, period=50):
    """
    Parameters
    ----------
    data: pandas dataframe
        Dataframe populated with prices.
    period: int
        Lookback period to compute the SMA. 50 by default.
    """
    SMA = data.rolling(window=period).mean()

    return SMA


def _std(data, period=50):
    """
    Parameters
    ----------
    data: pandas dataframe
        Dataframe populated with prices.
    period: int
        Lookback period to compute the SMA.
    """
    std = data.rolling(window=period)

    return std


def _PM(prices_df, sma_df):
    """
    Parameters
    ----------
    prices_df: pandas dataframe
        Dataframe containing prices.
    sma_df: pandas dataframe
     Dataframe containing sma data.
    """
    PM = (prices_df - sma_df) / sma_df

    return PM


def _bollinger_bands(data, periods=14, n=1.5,
                     column_name='close'):
    """
    It uses close prices.
    Parameters
    ----------
    data: pandas dataframe
        prices series data.
    periods: int
        Lockback period. 14 by default.
    n: int
        Number of standart deviations up and dowm from
        the std. 1.5 by default.
    """
    sma = _sma(data=data, period=periods)
    std = data.rolling(window=periods).std()
    upBand = sma + n*std
    downBand = sma - n*std

    return pd.DataFrame(index=data.index,
                        data={'close': data,
                              'sma': sma,
                              'Upper Band': upBand,
                              'Lower Band': downBand
                              }
                        )

def _rsi(data, periods=14):
    """
    Relative Strength Index

    Paramenters
    -----------
    data: pandas DataFrame
        Close prices.
    periods: int
        Number of candles to lookback.
    Returns
    -------
    rsi: series
        rsi values in series format
    """
    change = data.diff()
    
    gain = change.apply(lambda x: x if x>=0 else 0.0)
    loss = change.apply(lambda x: -x if x<0 else 0.0)
    
    avgGain = gain.ewm(span=periods, min_periods=periods).mean()
    avgLoss = loss.ewm(span=periods, min_periods=periods).mean()
    
    rs = avgGain / avgLoss
    rsi = 100 - (100/(rs + 1))

    return rsi

