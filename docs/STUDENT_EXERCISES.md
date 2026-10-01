# Make the project your own

Work through these personally. Predict the outcome first, then run the experiment and record what happened. Use a practice branch and temporary copies of logs/configuration. Commit actual changes when made; do not backdate work.

1. **Change a limit.** Copy `config/test_limits.json`, change voltage max from 3.6 to 3.5, and run with `--config`. Add a 3.55 V sample to a practice log so the difference is observable. Explain why the ordinary 3.3 V log still passes.
2. **Add a boundary test.** Add 3.6001 V to the parametrized test. Predict under/over flags, then run pytest. Explain why equality is accepted.
3. **Inject ERR.** Replace one voltage with `ERR`. Inspect the original CSV, imputed flag, quality counts and FAIL. Repeat at the first row and in a two-row gap to observe the fill limits.
4. **Remove temperature.** Delete the column from a copy. Explain the ERROR message and exit 2. Explain why a missing column differs from one corrupted reading.
5. **Change stuck duration.** Change `stuck_samples` to 8. The seven-value run in the supplied faulty log should stop counting as stuck. Explain why the log still fails other checks.
6. **Extend the specification.** On your practice branch, add temperature < -10 C as a new check and one unit test. Add configuration and report handling yourself. Explain that this deliberately extends the original six-check scope.
7. **Watch CI catch a defect.** On a practice branch, change the upper-voltage comparison to `>=`, push and inspect the failed boundary test in GitHub Actions. Restore the rule, push the fix and compare runs. Keep the real history.
8. **Create a Wokwi fault.** Run the circuit, change a knob, manually export CSV and analyze it. Identify exactly which evidence came from Wokwi and which came from the Python generator.
9. **Explain without notes.** In three minutes, draw the data flow, run healthy and faulty examples, point at a flagged row, and explain one limitation. Then modify a threshold and a test while someone watches.

For each exercise, keep a short note: prediction, command, observed result, explanation. A working repository is only the starting point; interview readiness means you can make and defend these changes yourself.
