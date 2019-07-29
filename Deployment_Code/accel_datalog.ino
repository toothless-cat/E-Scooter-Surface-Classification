const int zPin = 7;     // X output of the accelerometer
int start_time = millis();
int pulsez;
int accelerationz;

void setup() {
  // initialize serial communications:
  Serial.begin(9600);
  // initialize the pins connected to the accelerometer as inputs:
  pinMode(zPin, INPUT);
}


void loop() {
  //collect data every 20 millis, 50 readings per second
  //10 second worth of data
  if (millis()-start_time >=20){
    start_time = millis();
    pulsez = pulseIn(zPin, HIGH);
    accelerationz = (((pulsez / 10) - 500) * 8);
    Serial.print(accelerationz);
    Serial.print(",");
  }
}
