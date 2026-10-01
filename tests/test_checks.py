import numpy as np
import pandas as pd
import pytest
from hil_analyzer.checks import over_voltage, under_voltage, stuck_sensor, over_temperature, temperature_rate, sampling_gap


@pytest.mark.parametrize('value,under,over', [(2.99,True,False),(3.,False,False),(3.3,False,False),(3.6,False,False),(3.61,False,True)])
def test_voltage_boundaries(value, under, over):
    series = pd.Series([value])
    assert bool(under_voltage(series,3.).iloc[0]) == under
    assert bool(over_voltage(series,3.6).iloc[0]) == over


def test_stuck_run_is_retrospective_and_breaks_at_nan_or_gap():
    assert stuck_sensor(pd.Series([3.3]*4),5).sum() == 0
    assert stuck_sensor(pd.Series([3.3]*5),5).tolist() == [True]*5
    series = pd.Series([3.3,3.3,np.nan,3.3,3.3,3.3])
    assert stuck_sensor(series,5).sum() == 0
    assert stuck_sensor(pd.Series([3.3]*6),5,pd.Series([False,False,False,True,False,False])).sum() == 0


def test_temperature_limit_and_rate_use_real_timestamps():
    assert over_temperature(pd.Series([85.,85.01]),85).tolist() == [False,True]
    t = pd.Series([0.,.5,1.5,2.])
    rate = temperature_rate(t,25+2*t,2.5)
    assert np.allclose(rate,2)
    assert not (rate > 2).any()
    assert (temperature_rate(t,25+3*t,2.5) > 2).all()


def test_rate_does_not_bridge_gaps_or_missing_values():
    t = pd.Series([0.,1.,2.,8.,9.,10.])
    temp = pd.Series([25.,26.,np.nan,70.,71.,72.])
    rate = temperature_rate(t,temp,2.5)
    assert np.allclose(rate.dropna(),1)
    assert np.isnan(rate.iloc[2])


def test_sampling_gap_boundary():
    t = pd.Series([0.,1.,3.5,6.01])
    assert sampling_gap(t,2.5).tolist() == [False,False,False,True]
