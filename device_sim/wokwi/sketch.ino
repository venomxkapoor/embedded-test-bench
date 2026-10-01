// Simulated device under test (DUT) for the Wokwi online simulator (Arduino Uno).
// Two potentiometers act as sensors:
//   A0 -> "voltage"      (0-5 V)
//   A1 -> "temperature"  (0-100 degrees C, just a scaled value)
// Once per second the device prints one CSV line over the serial port.
// The same log format is read by run_analysis.py in the project root.

const int VOLTAGE_PIN = A0;
const int TEMP_PIN = A1;

void setup() {
  Serial.begin(115200);
  Serial.println("timestamp,voltage,temperature");  // CSV header
}

void loop() {
  // analogRead returns 0..1023 (10-bit ADC); scale it to physical units.
  float voltage = analogRead(VOLTAGE_PIN) * (5.0 / 1023.0);
  float temperature = analogRead(TEMP_PIN) * (100.0 / 1023.0);

  Serial.print(millis() / 1000.0, 1);  // timestamp in seconds
  Serial.print(",");
  Serial.print(voltage, 3);
  Serial.print(",");
  Serial.println(temperature, 2);

  delay(1000);  // 1 sample per second
}
