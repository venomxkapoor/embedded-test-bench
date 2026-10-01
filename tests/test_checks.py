import pandas as pd

from hil_analyzer.checks import moving_average, over_voltage, stuck_sensor, thermal_runaway


def test_over_voltage_flags_only_values_above_limit():
    df = pd.DataFrame({"voltage": [3.31, 3.71, 3.29, 3.85, 3.60]})
    assert over_voltage(df, 3.6).tolist() == [False, True, False, True, False]  # 3.60 is not > 3.6


def test_stuck_sensor_detects_long_run():
    s = pd.Series([3.30, 3.31, 3.28, 3.28, 3.28, 3.28, 3.28, 3.29, 3.30])
    assert stuck_sensor(s, min_repeats=5).tolist() == [
        False, False, True, True, True, True, True, False, False]


def test_stuck_sensor_ignores_short_repeat():
    s = pd.Series([3.30, 3.31, 3.31, 3.32])
    assert not stuck_sensor(s, min_repeats=5).any()


def test_thermal_runaway_flags_fast_rise():
    df = pd.DataFrame({
        "timestamp": list(range(10)),
        "temperature": [25, 25.1, 25.2, 25.3, 30, 35, 40, 41, 41.1, 41.2],
    })
    flags, _ = thermal_runaway(df, max_rate=2.0)
    assert flags.any()


def test_thermal_runaway_quiet_on_slow_drift():
    df = pd.DataFrame({"timestamp": list(range(10)),
                       "temperature": [25 + 0.05 * i for i in range(10)]})
    flags, _ = thermal_runaway(df, max_rate=2.0)
    assert not flags.any()


def test_moving_average_first_values_are_nan():
    out = moving_average(pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]), window=3)
    assert out.isna().tolist() == [True, True, False, False, False, False]
    assert out.iloc[2] == 2.0
