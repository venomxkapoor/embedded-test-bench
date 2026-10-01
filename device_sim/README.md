# Wokwi telemetry device

This is a simulated embedded device used to generate representative telemetry. The two knobs stand in for sensor inputs; neither is a calibrated temperature sensor or a measured power supply.

## Run

1. Open https://wokwi.com/projects/new/arduino-uno.
2. Replace `sketch.ino` with [this sketch](wokwi/sketch.ino).
3. Replace `diagram.json` with [this diagram](wokwi/diagram.json).
4. Start the simulation. The serial monitor prints `timestamp,voltage,temperature` and one row per second at 115200 baud.
5. Leave the default controls for around ten seconds. Voltage is near 3.3 V and temperature near 25 C.
6. Turn the voltage knob up until the reading exceeds 3.6 V. Turn the temperature knob above 85 C for another fault.
7. Copy the CSV header and desired complete serial rows into a plain text file, for example `logs/wokwi_capture.csv`. Remove terminal prompts or partial lines. This is a **manual export**, not a live Python connection.
8. Run `python run_analysis.py logs/wokwi_capture.csv --out-dir results/wokwi`.

To make separate healthy and fault logs, restart the simulation at the default knob values, copy a healthy window, then capture a fault window. Include the same CSV header in each file.

## Wiring and conversion

| Input | Uno pin | Scale |
| --- | --- | --- |
| Voltage pot SIG | A0 | raw ADC * 5 / 1023 V |
| Temperature pot SIG | A1 | raw ADC * 100 / 1023 C |
| Both VCC pins | 5V | Supply reference in the simulation |
| Both GND pins | GND | Common reference |

The Uno ADC returns a 10-bit integer, 0–1023. Scaling converts counts into demonstration engineering units. Firmware adds an explicit alternating ±0.003 V ripple to voltage. This is synthetic variation, not ADC noise. Removing that line makes an untouched knob trigger the five-identical-values rule. The sampling logic uses `millis()` and does not attempt a real-time scheduling guarantee.

The Python generator is an independent repeatable source for CI. Its random noise does not reproduce Wokwi's analogue model. Neither source establishes physical hardware performance.

References: [Uno](https://docs.wokwi.com/parts/wokwi-arduino-uno), [potentiometer](https://docs.wokwi.com/parts/wokwi-potentiometer), [serial monitor](https://docs.wokwi.com/guides/serial-monitor).
