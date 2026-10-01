# Study map for Project 1

Page numbers are PDF viewer pages starting at 1. Private study PDFs are not distributed here. The references identify practice topics, not completed coursework.

| Feature | Study reference | Apply here |
| --- | --- | --- |
| Parsing | `hil testing questions(python).pdf` A1 Q1 p1; A2 Q1-Q2 pp5-6 | Numeric text, exceptions, invalid versus failing readings |
| JSON | Same, A4 Q1-Q2 pp13-14; Q4-Q5 p15; Q7 pp16-17 | `config.py`, nested dictionaries, bad-key/type errors |
| Simulation | Same, A6 Q3-Q5 pp23-24; A5 Q8 p21 | Repeatable input; current generator is finite, not live serial |
| Thresholds | Same, A3 Q7 p12 | Inclusive accepted interval |
| ADC units | Same, A3 Q1 p9; Q4 pp10-11; `hil data questions.pdf` P13 p12 | Wokwi counts to volts and degrees |
| CSV cleaning | `hil data questions.pdf` C1-C5 pp1-3; P1 p8; P7 p10; P12-P13 p12 | Coercion, duplicates, sorting and quality evidence |
| Masks and rates | Same, N1 p3; N3-N4 p4; N9 pp5-6 | Boolean masks and timestamp-aware gradient |
| Repeated values | Same, P22 p15 | shift, run groups, retrospective flags |
| Plots | Same, M1-M6 p16; M9-M10 p17; M14 p18 | Units, limits, axes and PNG output |
| Test design | `a3_en.pdf` p1, Test Program and Hints | Wrong inputs, boundaries and independent expected values |
| Exit status | `a8_en.pdf` pp1-3 | Process result concepts applied to the Python CLI |
| MATLAB bridge | `introMatlab_course_notes_chapter_2.pdf` L-2.7 p7, L-2.8 p8, L-2.9 p9, L-2.15 p12 | Recreate a report plot independently |

## Additional topics

Learn pytest fixtures/parametrization, Git, one GitHub Actions workflow and basic Docker. SLP supplies useful testing, ADC and systems background. Interrupts and the solar controller belong to other work.

Use the official [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html), [GitHub Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python), and [Wokwi serial](https://docs.wokwi.com/guides/serial-monitor) guides.

## Fourteen study sessions

Allow 60-90 minutes each and repeat until the checkpoint is comfortable.

1. Run both examples and draw the pipeline from memory.
2. Practise Python lists, dictionaries, functions, exceptions and paths. Explain `main`.
3. Redo one-row parsing without solutions. Distinguish bad input from an out-of-range value.
4. Step through a six-row cleaning example. Explain why quality evidence survives repairs.
5. Load JSON and reject a bad key, type and reversed range.
6. Calculate voltage boundaries by hand. Complete exercises 1 and 2.
7. Draw repeated-run group numbers. Complete exercise 5 and explain false positives.
8. Calculate temperature slopes, then use irregular timestamps and missing data.
9. Recreate the report from CSV and explain plotted repairs.
10. Learn pytest fixtures, parametrization and tmp_path. Complete exercises 3, 4 and 6.
11. Learn ADC conversion, run Wokwi and complete exercise 8.
12. Learn git status/diff/add/commit/push. Complete exercise 7 on a practice branch.
13. Explain each Dockerfile line and run a clean checkout.
14. Complete exercise 9, answer the interview guide without notes and make one live change.

## Check answer keys critically

Python A3 Q1's arithmetic is 2.5150, not 2.5140; A3 Q6's XOR is 0x08, not 0x7E. Data N2 confuses noise standard deviation with the full noisy sine signal's standard deviation. Recalculate rather than memorise. Python A2 Q3 calls persistent out-of-range readings stuck; Data P22 means repeated identical values. This project uses the latter definition.

## Reading order

`run_analysis.py` -> `config.py` -> `cleaning.py` -> `checks.py` -> `analysis.py` -> `report.py` -> tests -> simulator -> workflow.

After each file, explain its purpose and one failure case. Complete the [student exercises](STUDENT_EXERCISES.md) and use the [interview guide](INTERVIEW_GUIDE.md). Reading alone is not interview readiness.
