# Explaining the sensor test bench

## A short introduction

“This project checks logs from a simulated sensor device. It reads voltage and temperature, validates the file, applies limits from JSON, and produces a PASS or FAIL report. I can inject known faults and use pytest to check the analyser itself. Wokwi demonstrates the microcontroller side; its serial output is copied into a CSV.”

Use that description once you can run and modify the work independently. Describe assistance honestly if asked. Do not claim physical hardware testing or completed learning exercises before doing them.

## Three minute demonstration

- **0:00–0:30:** Show the README diagram and explain the manual CSV boundary.
- **0:30–1:00:** Run the healthy log. Open its JSON verdict and plot.
- **1:00–1:45:** Run the faulty log. Show 3.75 V at 16 s in the raw data, its over-voltage flag, and exit 1. Counts can overlap.
- **1:45–2:15:** Open the five parametrized voltage boundaries and run pytest.
- **2:15–2:45:** Show the Wokwi circuit or screenshot, two inputs and serial records.
- **2:45–3:00:** Explain one limitation: a stable healthy signal can look stuck. Show the CI run and downloadable evidence.

## Beginner questions

**What problem does it solve?** It makes checking a sensor log repeatable and leaves evidence for a reviewer.

**What is a DUT?** Device under test. Here the device is simulated.

**Why Python?** It makes file handling, calculations, automated tests and plots straightforward in a small codebase.

**Why pandas?** A CSV becomes a table whose columns can be converted, compared, sorted and grouped.

**Why NumPy?** It provides numerical arrays and timestamp-aware gradient calculations; the generator also uses a seeded random source.

**Why pytest?** It runs independent assertions automatically and reports which expected behaviour changed.

**Why JSON limits?** Changing a demonstration threshold does not require editing a detector. Validation catches misspelled keys and impossible ranges.

**What causes PASS?** No sensor check and no input-quality rule may fail. Unusable input is ERROR, a separate exit status.

## Technical questions

**What does `pd.to_numeric(errors="coerce")` do?** It turns numeric text into numbers and invalid text into NaN. Infinity is also explicitly replaced with NaN here.

**Why corrupt CSV?** A device can reset, a capture can be incomplete, or text can be copied incorrectly. This project tests representative bad inputs; it does not validate a physical serial link.

**What does `shift()` do?** It aligns each reading with the previous reading. Equality tells us whether a repeated run continues. `cumsum()` assigns a group to each new run; group size gives the run length.

**When is a stuck run flagged?** All readings in a qualifying run are labelled offline. In a live detector we would only know at the fifth reading. Missing readings and long gaps break runs.

**What does `np.gradient` calculate?** Approximate slope, here degrees per second. Timestamps matter because a 4 C change over two seconds is different from the same change over one second. Interior and endpoint estimates differ. The code does not bridge bad sensor values or long time gaps.

**What is a sampling gap?** A difference between consecutive cleaned timestamps greater than 2.5 s by default. It suggests missing data but does not tell us the exact number of packets lost.

**Why exit 1?** Scripts and CI can recognise an intentionally failing DUT result without reading console text. Exit 0 means PASS; exit 2 means the analysis could not be performed. CI explicitly expects 1 for the faulty fixture.

**Why Agg?** It renders a PNG without opening a desktop window, so the same report works on a CI runner.

**What is parametrization?** One test function runs with several independently specified inputs and expected outputs, such as 2.99, 3.00, 3.30, 3.60 and 3.61 V.

**Unit versus end-to-end tests?** Unit tests isolate a rule or configuration function. End-to-end tests run a whole log through cleaning and analysis. The CLI test launches a real Python process and checks its exit code and files.

**What does GitHub Actions do?** On a push or pull request it installs dependencies, runs tests, checks example results, runs Docker and saves reports. It tests this repository, not a physical device.

**What does Docker solve?** It packages the Python runtime and dependencies so another machine can run the same command. It does not prove the sensor rules are correct or provide hardware access automatically.

## Engineering questions

**Why these thresholds?** They are explicit demonstration requirements, chosen to make boundary and fault examples easy to understand. A real product needs limits from its specification and measurement uncertainty.

**Where can stuck detection be wrong?** A stable or quantized good sensor can repeat. A frozen sensor with noise can vary. Exact equality is a simple heuristic, not a diagnosis.

**Why can forward-fill be dangerous?** It can make a missing measurement look like a real normal reading, or manufacture a repeated run. Here only isolated interior holes are filled for the plot, marked imputed, and excluded from checks; the original corruption still makes the verdict FAIL.

**What changes for physical hardware?** Add a real capture adapter, framing, timestamps, timeouts and disconnect handling. Verify units/calibration, wiring and actual device behaviour. Keep captured evidence and tests for the adapter.

**What changes for CAN?** Add a transport and message decoder, then requirements for IDs, counters and timing. That is a separate project; this repository has no CAN stack.

**One million rows?** Measure memory and runtime first. Chunked reading would need to carry the previous timestamp and repeated-run state across chunks. Gradient boundaries need neighbouring samples. Do not simply split the file and assume identical results.

**Malformed packets?** Test missing columns, extra fields, invalid numeric values, empty logs, duplicate and backwards timestamps. Decide whether to report a quality failure or reject the input; never accidentally report PASS.

**How is this different from HiL?** All device inputs are simulated and logs are analysed offline. Physical HiL includes a real controller interacting with a controlled environment through actual I/O, with timing and electrical behaviour to validate.

**What issue did review catch?** A gradient on irregular timestamps produced a tiny floating-point excess at exactly 2 C/s. Rounding calculated rates to 12 decimal places resolved the boundary ambiguity; the regression test stays in the suite. Reproduce and understand this before discussing it as your own debugging experience.

## CV wording after understanding the implementation

Embedded Sensor Test Automation Bench — Python, pytest, pandas, NumPy

- Developed a validation pipeline for simulated sensor telemetry with configurable limits and checks for voltage, temperature, repeated readings and sampling gaps.
- Added boundary and end-to-end tests, JSON/PNG reports, and automated GitHub Actions verification.
- Used a Wokwi Uno simulation to produce representative sensor telemetry for offline analysis.

Use only statements you can demonstrate. Keep the project date accurate, and distinguish completed work from future hardware plans.
