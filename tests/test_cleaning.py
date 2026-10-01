import numpy as np
import pytest
from hil_analyzer.cleaning import clean_log, load_log
from hil_analyzer.analysis import analyze


def test_missing_column_is_clear(good_frame):
    with pytest.raises(ValueError, match="missing required column 'temperature'"):
        clean_log(good_frame.drop(columns='temperature'))


def test_sort_duplicate_and_invalid_timestamp_are_recorded(good_frame):
    raw = good_frame.iloc[[2,0,1,1,3,4,5]].copy().reset_index(drop=True)
    raw.loc[0, 'timestamp'] = np.nan
    cleaned = clean_log(raw)
    assert cleaned.timestamp.tolist() == [0,1,3,4,5]
    assert cleaned.attrs['quality_issues']['duplicate_timestamp'] == 1
    assert cleaned.attrs['quality_issues']['invalid_timestamp'] == 1
    assert analyze(cleaned)['verdict'] == 'FAIL'
    assert clean_log(good_frame.iloc[::-1]).attrs['quality_issues']['unsorted_timestamp'] == 5


def test_bad_sensors_fill_only_isolated_holes(good_frame):
    raw = good_frame.astype({'voltage': object})
    raw.loc[1, 'voltage'] = 'ERR'
    raw.loc[3:4, 'voltage'] = ['NOISE', float('inf')]
    cleaned = clean_log(raw)
    assert cleaned.loc[1, 'voltage'] == 3.3
    assert cleaned.loc[1, 'voltage_imputed']
    assert cleaned.loc[3:4, 'voltage'].isna().all()
    result = analyze(cleaned)
    assert result['quality_issues']['invalid_voltage'] == 3
    assert result['verdict'] == 'FAIL'
    assert result['faults']['stuck_sensor'] == 0


def test_empty_or_unusable_input_rejected(good_frame):
    for frame in [good_frame.iloc[:0], good_frame.iloc[:1], good_frame.assign(timestamp=-1)]:
        with pytest.raises(ValueError):
            clean_log(frame)


def test_csv_loading_and_structural_errors(tmp_path):
    path = tmp_path / 'raw.csv'
    path.write_text('boot message\ntimestamp,voltage,temperature\n0,3.3,25\n1,3.31,25.1\n')
    assert len(load_log(path, skiprows=1)) == 2
    for text in ['', 'timestamp,voltage,voltage\n0,3,3', 'timestamp,voltage,temperature\n0,3,25,EXTRA\n']:
        path.write_text(text)
        with pytest.raises(ValueError, match='Invalid test log'):
            load_log(path)
    with pytest.raises(ValueError, match='skiprows'):
        load_log(path, -1)
