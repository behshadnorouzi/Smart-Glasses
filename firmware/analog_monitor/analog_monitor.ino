// Streams raw readings of one analog input over serial at a fixed rate,
// one integer per line. Used on the bench together with tools/serial_plot.

constexpr uint8_t kInputPin = A0;
constexpr unsigned long kBaudRate = 115200;
constexpr unsigned long kSamplePeriodMs = 50;  // 20 samples per second

void setup() {
  Serial.begin(kBaudRate);
}

void loop() {
  static unsigned long lastSampleMs = 0;

  const unsigned long now = millis();
  if (now - lastSampleMs >= kSamplePeriodMs) {
    lastSampleMs = now;
    Serial.println(analogRead(kInputPin));
  }
}
