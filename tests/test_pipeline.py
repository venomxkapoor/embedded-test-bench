"""End-to-end: generate a log, clean it, analyse it, check the verdict and the exit code."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from generate_sample_log import make_log  # noqa: E402
from hil_analyzer.analysis import analyze  # noqa: E402
from hil_analyzer.cleaning import clean_log  # noqa: E402
from run_analysis import main  # noqa: E402


def test_faulty_log_fails_and_reports_every_fault_type():
    findings = analyze(clean_log(make_log(healthy=False)))
    assert findings["verdict"] == "FAIL"
    assert findings["over_voltage_samples"] >= 3
    assert findings["stuck_sensor_samples"] >= 5
    assert findings["thermal_runaway_samples"] >= 1


def test_healthy_log_passes():
    findings = analyze(clean_log(make_log(healthy=True)))
    assert findings["verdict"] == "PASS"


def test_cli_exit_code_matches_verdict(tmp_path):
    bad, good = tmp_path / "bad.csv", tmp_path / "good.csv"
    make_log(healthy=False).to_csv(bad, index=False)
    make_log(healthy=True).to_csv(good, index=False)
    assert main([str(bad), "--out", str(tmp_path / "bad.png")]) == 1
    assert main([str(good), "--out", str(tmp_path / "good.png")]) == 0
    assert (tmp_path / "bad.png").exists()
