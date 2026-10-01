"""Offline telemetry validation: 0 PASS, 1 FAIL, 2 input/configuration error."""
import argparse
import json
from pathlib import Path
import sys
from hil_analyzer.analysis import analyze
from hil_analyzer.cleaning import clean_log, load_log
from hil_analyzer.config import load_config
from hil_analyzer.report import write_report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', help='CSV captured from the simulated DUT')
    parser.add_argument('--config', help='JSON limit overrides')
    parser.add_argument('--skiprows', type=int, default=0, help='skip N boot-text lines')
    parser.add_argument('--out-dir', default='results', help='JSON, CSV and PNG output directory')
    args = parser.parse_args(argv)
    out = Path(args.out_dir)
    try:
        limits = load_config(args.config)
        df = clean_log(load_log(args.log, skiprows=args.skiprows))
        findings = analyze(df, limits)
        write_report(df, findings, out)
    except (ValueError, OSError, UnicodeError) as exc:
        try:
            out.mkdir(parents=True, exist_ok=True)
            (out / 'result.json').write_text(json.dumps({'verdict': 'ERROR', 'error': str(exc)}, indent=2) + '\n', encoding='utf-8')
            # Prevent an old PASS plot being mistaken for evidence from this run.
            for name in ('samples.csv', 'report.png'):
                (out / name).unlink(missing_ok=True)
        except OSError:
            pass
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print('Embedded Device Validation Report')
    print(f"Samples analysed: {findings['samples']}")
    for name, count in findings['faults'].items():
        print(f'{name:26} {count}')
    print(f"Input-quality rows: {findings['quality_issue_samples']}")
    print(f"VERDICT: {findings['verdict']} (reports: {out})")
    return 0 if findings['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
