"""Create a synthetic test log with known problems injected, so the analyzer has something to find.

Usage:  python scripts/generate_sample_log.py logs/sample_log.csv
        python scripts/generate_sample_log.py logs/healthy_log.csv --healthy
"""
import argparse

import numpy as np
import pandas as pd


def make_log(healthy=False, seed=42, n=120):
    rng = np.random.default_rng(seed)  # fixed seed -> same file every time (reproducible)
    t = np.arange(n, dtype=float)                       # 1 sample per second
    voltage = 3.30 + rng.normal(0, 0.02, n)             # nominal 3.3 V plus noise
    temperature = 25.0 + 0.02 * t + rng.normal(0, 0.05, n)

    if not healthy:
        voltage[40:43] = 3.75                            # over-voltage spike
        voltage[70:77] = 3.300                           # stuck sensor: 7 identical values
        temperature[100:110] = temperature[100] + 3.0 * np.arange(10)  # fast temperature rise

    df = pd.DataFrame({"timestamp": t, "voltage": voltage.round(3),
                       "temperature": temperature.round(2)})

    # Make it messy like a real log: junk strings, gaps, one duplicated row
    df = df.astype({"voltage": object, "temperature": object})
    df.loc[15, "voltage"] = "NOISE"
    df.loc[16, "temperature"] = "ERR"
    df.loc[25, "voltage"] = None
    df = pd.concat([df, df.iloc[[30]]], ignore_index=True)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out")
    parser.add_argument("--healthy", action="store_true", help="no injected faults")
    args = parser.parse_args()
    make_log(healthy=args.healthy).to_csv(args.out, index=False)
    print(f"wrote {args.out}")
