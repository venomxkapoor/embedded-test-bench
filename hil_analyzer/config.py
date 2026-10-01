"""Load and validate the small JSON test specification."""
import copy
import json
import math
from pathlib import Path

DEFAULT_LIMITS = {
    "voltage": {"min": 3.0, "max": 3.6, "stuck_samples": 5},
    "temperature": {"max": 85.0, "max_rise_rate": 2.0},
    "sampling": {"expected_interval_seconds": 1.0, "max_gap_seconds": 2.5},
}


def validate_limits(overrides=None):
    limits = copy.deepcopy(DEFAULT_LIMITS)
    if overrides is None:
        return limits
    if not isinstance(overrides, dict):
        raise ValueError("Invalid configuration: expected a JSON object")
    for group, values in overrides.items():
        if group not in limits or not isinstance(values, dict):
            raise ValueError(f"Invalid configuration group: {group}")
        for key, value in values.items():
            if key not in limits[group]:
                raise ValueError(f"Unknown configuration key: {group}.{key}")
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"Configuration {group}.{key} must be a finite number")
            limits[group][key] = value
    v, t, s = limits['voltage'], limits['temperature'], limits['sampling']
    if v['min'] < 0 or v['min'] >= v['max']:
        raise ValueError("Voltage limits require 0 <= min < max")
    if type(v['stuck_samples']) is not int or v['stuck_samples'] < 2:
        raise ValueError("stuck_samples must be an integer >= 2")
    if t['max_rise_rate'] <= 0 or s['expected_interval_seconds'] <= 0:
        raise ValueError("Rise rate and expected interval must be positive")
    if s['max_gap_seconds'] < s['expected_interval_seconds']:
        raise ValueError("max_gap_seconds must be >= expected_interval_seconds")
    return limits


def load_config(path=None):
    if path is None:
        path = Path(__file__).resolve().parent.parent / 'config' / 'test_limits.json'
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('Invalid configuration: expected a JSON object')
        return validate_limits(data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON configuration: {exc.msg}") from exc
