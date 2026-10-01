# Simulated device (Wokwi)

A simulated Arduino Uno with two potentiometers stands in for a real device under test.
**This is a simulation, not real hardware.**

## Run it
1. Go to https://wokwi.com and start a new Arduino Uno project.
2. Replace the contents of `sketch.ino` and `diagram.json` with the files in `wokwi/`.
   (The wiring in `diagram.json` is untested - if Wokwi complains about a pin name, wire the
   parts by hand: each pot's SIG to A0 / A1, VCC to 5V, GND to GND.)
3. Press play. Turn the potentiometers while it runs - that is your "fault injection".
4. Copy the serial monitor output into `logs/wokwi_run.csv` (keep the header line).
5. Analyse it:  `python run_analysis.py logs/wokwi_run.csv --out docs/wokwi_report.png`

## Things to try
- Turn the voltage pot above ~72 % -> over-voltage FAIL (3.6 V limit).
- Leave a pot untouched for 5+ seconds -> "stuck sensor" flag. Is that a real fault, or just
  a steady signal? (Good interview discussion: the limits of this check.)
- Turn the temperature pot quickly -> thermal-runaway flag.

## Add your own evidence
Screenshot the running simulation and the resulting report into `docs/` and label them
"simulated". Real photos only if you later build it on a real board.
