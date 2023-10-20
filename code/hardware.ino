#define analogIn  A0 // select the input pin
int value = 0; // variable to store the value coming from the sensor

void setup()
{
  Serial.begin(115200); // open serial port, set the baud rate to 115200 bps
}

void loop()
{

  value = analogRead(analogIn); // read the value from the sensor
  Serial.println(value); // print the value to the serial monitor
}
