import pandas as pd

from hil_analyzer.cleaning import clean_log, load_log


def test_junk_strings_become_numbers_or_are_filled():
    raw = pd.DataFrame({
        "timestamp": [0, 1, 2],
        "voltage": ["3.3", "NOISE", "3.4"],
        "temperature": [25.0, 25.1, "ERR"],
    })
    out = clean_log(raw)
    assert out["voltage"].tolist() == [3.3, 3.3, 3.4]          # NOISE -> forward-filled
    assert out["temperature"].tolist() == [25.0, 25.1, 25.1]   # ERR -> forward-filled


def test_duplicates_dropped_and_sorted():
    raw = pd.DataFrame({
        "timestamp": [2, 0, 1, 1],
        "voltage": [3.3, 3.3, 3.3, 3.3],
        "temperature": [25, 25, 25, 25],
    })
    out = clean_log(raw)
    assert out["timestamp"].tolist() == [0, 1, 2]


def test_rows_with_no_value_at_start_are_dropped():
    raw = pd.DataFrame({
        "timestamp": [0, 1],
        "voltage": [None, 3.3],
        "temperature": [25, 25],
    })
    out = clean_log(raw)
    assert out["timestamp"].tolist() == [1]


def test_load_log_skips_boot_noise(tmp_path):
    f = tmp_path / "log.csv"
    f.write_text("garbage\nmore garbage\ntimestamp,voltage,temperature\n0,3.3,25\n1,3.31,25\n")
    df = load_log(f, skiprows=2)
    assert list(df.columns) == ["timestamp", "voltage", "temperature"]
    assert len(df) == 2
