"""Six offline checks. Equality at a limit is accepted."""
import numpy as np
import pandas as pd


def over_voltage(series, limit):
    return series > limit


def under_voltage(series, limit):
    return series < limit


def over_temperature(series, limit):
    return series > limit


def stuck_sensor(series, min_repeats=5, breaks=None):
    # Runs are marked retrospectively, including their first sample.
    same = series.eq(series.shift()) & series.notna()
    if breaks is not None:
        same &= ~breaks
    groups = (~same).cumsum()
    lengths = series.groupby(groups).transform('size')
    return (lengths >= min_repeats) & series.notna()


def sampling_gap(timestamp, max_gap):
    return timestamp.diff() > max_gap


def temperature_rate(timestamp, temperature, max_gap):
    # Never differentiate across missing sensor values or a sampling gap.
    valid = temperature.notna()
    breaks = (~valid) | (~valid.shift(1, fill_value=False)) | (timestamp.diff() > max_gap)
    groups = breaks.cumsum()
    rate = pd.Series(np.nan, index=timestamp.index, dtype=float)
    for _, segment in timestamp[valid].groupby(groups[valid]):
        ix = segment.index
        if len(ix) >= 2:
            rate.loc[ix] = np.gradient(temperature.loc[ix].to_numpy(), segment.to_numpy())
    # Ignore sub-picounit numerical noise at an exact configured boundary.
    return rate.round(12)
