"""Combine the checks into one pass/fail verdict."""
from .checks import over_voltage, stuck_sensor, thermal_runaway

DEFAULT_LIMITS = {
    "voltage_limit": 3.6,      # volts
    "stuck_min_repeats": 5,    # identical samples in a row
    "max_temp_rate": 2.0,      # degrees per second
}


def analyze(df, limits=None):
    """Run all checks on a cleaned log and return a findings dict."""
    lim = {**DEFAULT_LIMITS, **(limits or {})}
    ov = over_voltage(df, lim["voltage_limit"])
    stuck = stuck_sensor(df["voltage"], lim["stuck_min_repeats"])
    runaway, rate = thermal_runaway(df, lim["max_temp_rate"])

    findings = {
        "samples": len(df),
        "over_voltage_samples": int(ov.sum()),
        "stuck_sensor_samples": int(stuck.sum()),
        "thermal_runaway_samples": int(runaway.sum()),
        "masks": {"over_voltage": ov, "stuck": stuck, "runaway": runaway},
        "temp_rate": rate,
        "limits": lim,
    }
    failed = any(
        findings[k] > 0
        for k in ("over_voltage_samples", "stuck_sensor_samples", "thermal_runaway_samples")
    )
    findings["verdict"] = "FAIL" if failed else "PASS"
    return findings
