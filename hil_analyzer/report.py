"""Write headless plots and portable test evidence."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_report(df, findings, out_path):
    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
    x = df.timestamp
    lim, masks = findings['limits'], findings['masks']
    for ax in axes:
        ax.grid(alpha=.18)
        ax.spines[['top', 'right']].set_visible(False)
    axes[0].plot(x, df.voltage, '.-', color='#147d76', lw=1, label='Voltage')
    for value in (lim['voltage']['min'], lim['voltage']['max']):
        axes[0].axhline(value, color='#b53c35', ls='--', lw=1)
    bad = masks['over_voltage'] | masks['under_voltage'] | masks['stuck_sensor']
    axes[0].scatter(x[bad], df.voltage[bad], color='#c94b43', zorder=3, label='Flagged')
    axes[0].set_ylabel('Voltage [V]')
    axes[0].legend(loc='upper right', fontsize=8)
    axes[1].plot(x, df.temperature, '.-', color='#c27b20', lw=1)
    axes[1].axhline(lim['temperature']['max'], color='#b53c35', ls='--', lw=1)
    bad = masks['over_temperature'] | masks['rapid_temperature_rise']
    axes[1].scatter(x[bad], df.temperature[bad], color='#c94b43', zorder=3)
    axes[1].set_ylabel('Temperature [deg C]')
    axes[2].plot(x, findings['temp_rate'], '.-', color='#456498', lw=1)
    axes[2].axhline(lim['temperature']['max_rise_rate'], color='#b53c35', ls='--', lw=1)
    axes[2].set_ylabel('Rise rate [deg C/s]')
    axes[2].set_xlabel('Device timestamp [s]')
    for timestamp in x[masks['sampling_gap']]:
        for ax in axes:
            ax.axvline(timestamp, color='#777777', ls=':', alpha=.6)
    fig.suptitle(f"Simulated DUT telemetry | {findings['verdict']}", x=.09, ha='left', fontsize=17, weight='bold')
    fig.text(.09, .925, f"{len(df)} analysed rows | {findings['quality_issue_samples']} input-quality rows | dashed lines: limits; vertical dotted lines: gaps", fontsize=9)
    fig.text(.09, .022, 'Synthetic / simulator data. Repairs do not erase input-quality failures. See result.json and samples.csv.', fontsize=9, color='#555555')
    fig.tight_layout(rect=(.025,.04,1,.91))
    target = Path(out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target, dpi=140)
    plt.close(fig)


def write_report(df, findings, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary = {k: v for k, v in findings.items() if k not in ('masks', 'temp_rate')}
    (out / 'result.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    rows = df.copy()
    for name, mask in findings['masks'].items():
        rows['flag_' + name] = mask
    rows['temperature_rate_c_per_s'] = findings['temp_rate']
    rows.to_csv(out / 'samples.csv', index=False)
    plot_report(df, findings, out / 'report.png')
