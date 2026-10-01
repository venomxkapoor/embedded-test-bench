import json
import subprocess
import sys
from pathlib import Path
import pytest
from hil_analyzer.analysis import analyze
from hil_analyzer.cleaning import clean_log
from run_analysis import main
from scripts.generate_sample_log import make_log


def test_healthy_end_to_end():
    result = analyze(clean_log(make_log('healthy')))
    assert result['verdict'] == 'PASS'
    assert not any(result['faults'].values())


def test_faulty_end_to_end_detects_all_six_checks():
    result = analyze(clean_log(make_log('faulty')))
    assert result['verdict'] == 'FAIL'
    assert all(count > 0 for count in result['faults'].values())


def test_each_fault_scenario_and_repeatability():
    names = ['over_voltage','under_voltage','stuck_sensor','over_temperature','rapid_temperature_rise','sampling_gap']
    for name in names:
        assert analyze(clean_log(make_log(name)))['faults'][name] > 0
    assert make_log().equals(make_log())
    assert analyze(clean_log(make_log('malformed')))['verdict'] == 'FAIL'
    with pytest.raises(ValueError):
        make_log('unknown')


def test_cli_real_process_exit_codes_and_reports(tmp_path):
    root = Path(__file__).resolve().parents[1]
    for scenario,code in [('healthy',0),('faulty',1)]:
        log=tmp_path/(scenario+'.csv')
        make_log(scenario).to_csv(log,index=False)
        out=tmp_path/scenario
        proc=subprocess.run([sys.executable,str(root/'run_analysis.py'),str(log),'--out-dir',str(out)],capture_output=True,text=True)
        assert proc.returncode == code, proc.stderr
        data=json.loads((out/'result.json').read_text())
        assert data['verdict'] == ('PASS' if code == 0 else 'FAIL')
        assert (out/'report.png').read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
        assert (out/'samples.csv').exists()


def test_cli_error_replaces_stale_success(tmp_path,capsys):
    log=tmp_path/'log.csv';out=tmp_path/'results'
    make_log().to_csv(log,index=False)
    assert main([str(log),'--out-dir',str(out)]) == 0
    log.write_text('timestamp,voltage\n0,3.3\n')
    assert main([str(log),'--out-dir',str(out)]) == 2
    assert 'missing required column' in capsys.readouterr().err
    assert json.loads((out/'result.json').read_text())['verdict'] == 'ERROR'
    assert not (out/'report.png').exists()


def test_analyze_rejects_unclean_time_order(good_frame):
    with pytest.raises(ValueError,match='strictly increasing'):
        analyze(clean_log(good_frame).iloc[::-1])
