"""Individual checks. Each one takes data and returns a True/False flag per sample."""
import numpy as np
import pandas as pd


def over_voltage(df, limit=3.6):
    """True where the voltage is above the limit (boolean masking, no loop)."""
    return df["voltage"] > limit


def stuck_sensor(series, min_repeats=5):
    """True for every sample inside a run of >= min_repeats identical values.

    How it works:
      - series.shift(1) is the previous value, so `series == series.shift(1)`
        says "same as before?".
      - Every time the value changes, a new run starts; cumsum() gives each run an id.
      - groupby(...).transform("size") gives the length of the run each sample is in.
    Note: comparing floats with == is only safe because ADC readings are discrete.
    """
    same_as_previous = series == series.shift(1)
    run_id = (~same_as_previous).cumsum()
    run_length = series.groupby(run_id).transform("size")
    return run_length >= min_repeats


def thermal_runaway(df, max_rate=2.0):
    """Flag samples where temperature rises faster than max_rate degrees/second.

    np.gradient computes the rate of change; passing the timestamps as the second
    argument makes it correct even if samples are not evenly spaced.
    Returns (flags, rate) as two Series.
    """
    rate = np.gradient(df["temperature"].to_numpy(), df["timestamp"].to_numpy())
    rate = pd.Series(rate, index=df.index)
    return rate > max_rate, rate


def moving_average(series, window=5):
    """Smoothed signal for plotting. The first window-1 values are NaN."""
    return series.rolling(window=window).mean()
