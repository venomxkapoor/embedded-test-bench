"""Deterministic synthetic telemetry for repeatable tests; no serial hardware."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

SCENARIOS = ('healthy', 'over_voltage', 'under_voltage', 'stuck_sensor',
             'over_temperature', 'rapid_temperature_rise', 'sampling_gap', 'malformed', 'faulty')


def make_log(scenario='healthy', seed=7):
    if scenario not in SCENARIOS:
        raise ValueError(f'Unknown scenario: {scenario}')
    rng = np.random.default_rng(seed)
    timestamp = np.arange(120, dtype=float)
    voltage = np.round(3.30 + rng.normal(0, .008, 120), 3)
    temperature = np.round(25 + .04 * timestamp + rng.normal(0, .02, 120), 2)
    df = pd.DataFrame({'timestamp': timestamp, 'voltage': voltage, 'temperature': temperature})
    if scenario in ('over_voltage', 'faulty'):
        df.loc[15:17, 'voltage'] = [3.72, 3.75, 3.74]
    if scenario in ('under_voltage', 'faulty'):
        df.loc[25:26, 'voltage'] = [2.95, 2.97]
    if scenario in ('stuck_sensor', 'faulty'):
        df.loc[35:41, 'voltage'] = 3.31
    if scenario in ('over_temperature', 'faulty'):
        # Offset a whole segment; the edge also legitimately triggers a rise fault.
        df.loc[65:69, 'temperature'] = [86, 86.2, 86.4, 86.6, 86.8]
    if scenario in ('rapid_temperature_rise', 'faulty'):
        df.loc[80:85, 'temperature'] = [30, 34, 38, 42, 46, 50]
    if scenario in ('sampling_gap', 'faulty'):
        df = df.drop(index=range(100, 105))
    if scenario == 'malformed':
        df['voltage'] = df.voltage.astype(object)
        df.loc[10, 'voltage'] = 'ERR'
    return df.reset_index(drop=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', choices=SCENARIOS)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if bool(args.scenario) != bool(args.out):
        parser.error('--scenario and --out must be used together')
    targets = [(args.scenario, args.out)] if args.scenario else [('healthy', Path('logs/healthy_log.csv')), ('faulty', Path('logs/faulty_log.csv'))]
    for scenario, target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        make_log(scenario).to_csv(target, index=False)
        print(target)


if __name__ == '__main__':
    main()
