"""Repair a plotting view while retaining data-quality evidence for the verdict."""
import csv
import warnings
import numpy as np
import pandas as pd

NUMERIC_COLUMNS = ['timestamp', 'voltage', 'temperature']


def load_log(path, skiprows=0):
    if type(skiprows) is not int or skiprows < 0:
        raise ValueError('skiprows must be a non-negative integer')
    # Check header duplicates before pandas renames them automatically.
    with open(path, encoding='utf-8-sig', newline='') as stream:
        for _ in range(skiprows):
            next(stream, None)
        header = next(csv.reader(stream), [])
    if len(header) != len(set(header)):
        raise ValueError('Invalid test log: duplicate column names')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', pd.errors.ParserWarning)
            return pd.read_csv(path, skiprows=skiprows, dtype=str, index_col=False,
                               skip_blank_lines=False, encoding='utf-8-sig')
    except (pd.errors.ParserError, pd.errors.EmptyDataError, pd.errors.ParserWarning) as exc:
        raise ValueError(f'Invalid test log: malformed CSV ({exc})') from exc


def clean_log(df):
    missing = [col for col in NUMERIC_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Invalid test log: missing required column '{missing[0]}'")
    if df.empty:
        raise ValueError('Invalid test log: no data rows')
    out = df[NUMERIC_COLUMNS].copy()
    out['source_row'] = np.arange(1, len(out) + 1)
    for col in NUMERIC_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors='coerce')
        out[col] = out[col].where(np.isfinite(out[col]))
    out.loc[out.timestamp < 0, 'timestamp'] = np.nan
    invalid = out[NUMERIC_COLUMNS].isna()
    duplicate = out.timestamp.notna() & out.timestamp.duplicated(keep='first')
    backwards = out.timestamp.diff().lt(0)
    issues = {'invalid_timestamp': int(invalid.timestamp.sum()),
              'invalid_voltage': int(invalid.voltage.sum()),
              'invalid_temperature': int(invalid.temperature.sum()),
              'duplicate_timestamp': int(duplicate.sum()),
              'unsorted_timestamp': int(backwards.sum())}
    quality_rows = int((invalid.any(axis=1) | duplicate | backwards).sum())
    out = out.dropna(subset=['timestamp']).drop_duplicates('timestamp', keep='first')
    out = out.sort_values('timestamp').reset_index(drop=True)
    for col in ['voltage', 'temperature']:
        # Only an isolated interior hole is filled, and only for visual continuity.
        good = out[col].notna()
        fill = ~good & good.shift(1, fill_value=False) & good.shift(-1, fill_value=False)
        out[col + '_imputed'] = fill
        out.loc[fill, col] = out[col].ffill().loc[fill]
    if len(out) < 2:
        raise ValueError('Invalid test log: at least two distinct usable timestamps are required')
    out.attrs.update(quality_issues=issues, quality_issue_samples=quality_rows, raw_samples=len(df))
    return out
