"""Load and clean raw test logs. Real logs are messy, so this is the first step."""
import pandas as pd

NUMERIC_COLUMNS = ["timestamp", "voltage", "temperature"]


def load_log(path, skiprows=0):
    """Read a CSV log.

    skiprows: number of garbage lines (e.g. boot noise) before the real header.
    """
    return pd.read_csv(path, skiprows=skiprows)


def clean_log(df):
    """Return a cleaned copy of a raw log.

    Steps:
      1. Convert columns to numbers. Junk such as 'NOISE' or 'ERR' becomes NaN
         (errors="coerce") instead of crashing the script.
      2. Drop rows without a usable timestamp.
      3. Drop duplicate timestamps and sort by time.
      4. Forward-fill short gaps in the sensor values (last known value).
      5. Drop rows that still have no value (e.g. gap at the very start).
    """
    out = df.copy()
    for col in NUMERIC_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=["timestamp"])
    out = out.drop_duplicates(subset="timestamp")
    out = out.sort_values("timestamp").reset_index(drop=True)
    out[["voltage", "temperature"]] = out[["voltage", "temperature"]].ffill()
    out = out.dropna(subset=["voltage", "temperature"]).reset_index(drop=True)
    return out
