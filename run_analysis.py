"""Command line entry point:  python run_analysis.py logs/sample_log.csv

Exit code 0 = PASS, 1 = FAIL. CI servers use the exit code to decide whether a test run passed.
"""
import argparse
import sys

from hil_analyzer.analysis import analyze
from hil_analyzer.cleaning import clean_log, load_log
from hil_analyzer.report import plot_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analyse a device test log.")
    parser.add_argument("log", help="path to the CSV log")
    parser.add_argument("--skiprows", type=int, default=0, help="garbage lines before the header")
    parser.add_argument("--out", default="report.png", help="output PNG path")
    args = parser.parse_args(argv)

    df = clean_log(load_log(args.log, skiprows=args.skiprows))
    findings = analyze(df)
    plot_report(df, findings, args.out)

    print(f"Samples analysed:        {findings['samples']}")
    print(f"Over-voltage samples:    {findings['over_voltage_samples']}")
    print(f"Stuck-sensor samples:    {findings['stuck_sensor_samples']}")
    print(f"Thermal-runaway samples: {findings['thermal_runaway_samples']}")
    print(f"VERDICT: {findings['verdict']}  (report: {args.out})")
    return 0 if findings["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
