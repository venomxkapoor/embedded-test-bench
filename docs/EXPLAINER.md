# Learn this project (read before you show it to anyone)

## Reading order (about 2-3 hours)
1. `run_analysis.py` - the entry point; follow what it calls.
2. `hil_analyzer/cleaning.py` - what each cleaning step fixes.
3. `hil_analyzer/checks.py` - the three checks; the stuck-sensor one is the tricky one.
4. `hil_analyzer/analysis.py` and `report.py`.
5. `tests/` - what each test proves, and why its input was chosen.

## Questions you should be able to answer
- Why `pd.to_numeric(errors="coerce")` instead of letting it crash?
- Why forward-fill instead of dropping rows? When would that be wrong?
- How does `shift(1)` + `cumsum()` find a run of identical values?
- Why pass timestamps to `np.gradient`?
- Why `matplotlib.use("Agg")`?
- Why does the CLI exit with code 1 on FAIL?
- What is the difference between SiL (simulated) and HiL (real hardware in the loop)?
- What would change if the data came from a real device instead of a simulator?
- Where can this tool give a false alarm? (hint: a steady, healthy signal)

## Your turn - do these before you claim the project
1. **Change a limit** (e.g. voltage 3.5 V) and predict how the verdict changes *before* running.
2. **Add a check**: a voltage-too-low check (below 3.0 V) with its own unit test.
3. **Break it on purpose**: feed a log with a missing column. Read the error, then make the
   loader fail with a clear message, and add a test for that.
4. **Run the simulator** (`device_sim/README.md`), inject faults, analyse your own log.
5. **Explain it out loud**, 3 minutes, without looking at the code. Record yourself if you can.

If you can do these five, the project is genuinely yours.
