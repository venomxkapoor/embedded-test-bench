import json
import pytest
from hil_analyzer.config import load_config, validate_limits


def test_defaults_and_json_override(tmp_path):
    config = tmp_path / 'limits.json'
    config.write_text(json.dumps({'voltage': {'max': 3.5}}))
    assert load_config(config)['voltage']['max'] == 3.5
    assert load_config()['voltage']['max'] == 3.6


def test_rejects_bad_configuration(tmp_path):
    for value in [[], {'typo': {}}, {'voltage': []}, {'voltage': {'typo': 1}},
                  {'voltage': {'min': 4}}, {'voltage': {'max': True}},
                  {'voltage': {'max': float('nan')}}, {'voltage': {'stuck_samples': 1.5}},
                  {'temperature': {'max_rise_rate': 0}}, {'sampling': {'max_gap_seconds': .5}}]:
        with pytest.raises(ValueError):
            validate_limits(value)
    broken = tmp_path / 'broken.json'
    broken.write_text('{')
    with pytest.raises(ValueError, match='Invalid JSON'):
        load_config(broken)


def test_defaults_are_not_mutated():
    first = validate_limits()
    first['voltage']['max'] = 9
    assert validate_limits()['voltage']['max'] == 3.6
