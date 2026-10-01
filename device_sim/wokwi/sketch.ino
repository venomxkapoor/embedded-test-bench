// Simulated DUT: two test inputs, one CSV record per second.
// A0 maps to 0..5 V; A1 maps to 0..100 deg C (not a calibrated sensor).
unsigned long lastSample = 0;
unsigned long sample = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("timestamp,voltage,temperature");
}

void loop() {
  unsigned long now = millis();
  if (now - lastSample < 1000) return;
  lastSample = now;
  float voltage = analogRead(A0) * (5.0f / 1023.0f);
  float temperature = analogRead(A1) * (100.0f / 1023.0f);
  // Explicit synthetic ripple avoids a perfectly fixed pot looking stuck.
  // Remove this line to demonstrate the repeated-value detector.
  voltage += (sample % 2 == 0) ? -0.003f : 0.003f;
  sample++;
  Serial.print(now / 1000.0f, 3);
  Serial.print(',');
  Serial.print(voltage, 3);
  Serial.print(',');
  Serial.println(temperature, 2);
}
