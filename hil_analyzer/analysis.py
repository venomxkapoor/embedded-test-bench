"""Combine six checks and input quality into a conservative verdict."""
from .config import validate_limits
from .checks import over_voltage, under_voltage, over_temperature, stuck_sensor, sampling_gap, temperature_rate


def analyze(df, limits=None):
    lim = validate_limits(limits)
    if len(df) < 2 or not df.timestamp.is_monotonic_increasing or df.timestamp.duplicated().any():
        raise ValueError('analyze requires at least two cleaned, strictly increasing timestamps')
    voltage = df.voltage.mask(df.voltage_imputed)
    temperature = df.temperature.mask(df.temperature_imputed)
    gaps = sampling_gap(df.timestamp, lim['sampling']['max_gap_seconds'])
    rate = temperature_rate(df.timestamp, temperature, lim['sampling']['max_gap_seconds'])
    masks = {
        'over_voltage': over_voltage(voltage, lim['voltage']['max']),
        'under_voltage': under_voltage(voltage, lim['voltage']['min']),
        'stuck_sensor': stuck_sensor(voltage, lim['voltage']['stuck_samples'], gaps),
        'over_temperature': over_temperature(temperature, lim['temperature']['max']),
        'rapid_temperature_rise': rate > lim['temperature']['max_rise_rate'],
        'sampling_gap': gaps,
    }
    faults = {name: int(mask.sum()) for name, mask in masks.items()}
    quality = df.attrs.get('quality_issues', {})
    failed = any(faults.values()) or any(quality.values())
    return {'samples': len(df), 'raw_samples': df.attrs.get('raw_samples', len(df)),
            'verdict': 'FAIL' if failed else 'PASS', 'faults': faults,
            'quality_issues': quality, 'quality_issue_samples': df.attrs.get('quality_issue_samples', 0),
            'limits': lim, 'masks': masks, 'temp_rate': rate}
