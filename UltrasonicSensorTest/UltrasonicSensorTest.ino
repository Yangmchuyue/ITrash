/* This is a program that reads the ultrasonic sensor values. 
 * How it works:
 *  1. The arduino sends a signal to the ultrasonic sensor (via. trigger pin) to send out a sound wave.
 *  2. When the wave hits an object and bounces back, the sensor picks up the "echo" and relays the information back to the arduino (via. echo pin).
 *  3. Based on the time it took for the sound wave to be reflected back, the arduino calculates the distance from the object.
 *  
 * References: 
 * -https://howtomechatronics.com/tutorials/arduino/ultrasonic-sensor-hc-sr04/
 * -https://forum.arduino.cc/index.php?topic=94499.0
 * -http://www.robotc.net/wikiarchive/Tutorials/Arduino_Projects/Mobile_Robotics/VEX/Use_Ultrasonic_Sensor_To_Measure_Distance
 * -https://www.arduino.cc/reference/en/language/functions/communication/serial/
 */
 
const int trigPin = 7;
const int echoPin = 8;

long duration;
long distance;

void setup() {
  Serial.begin(9600); //opens serial port to communicate with computer and sets the data rate to 9600 bps. This allows us to view the sensor readings.
  pinMode(trigPin, OUTPUT); //initialize the trigger pin as an output
  pinMode(echoPin, INPUT);  //initialize the echo pin as an input
}

void loop() {
  //Clearing the trigPin by setting it on a LOW state for 2 microseconds
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  //Sending the ultrasound wave by setting the trigPin on a HIGH state for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  //Reading the echoPin to obtain the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  //Calculating the distance from object
  distance = (0.034*duration)/2; //speed of sound is 0.034cm/microsecond -> d = v*t = 0.034*t/2 (divide by 2 because the wave travels d distance twice)
  
  //Printing the distance on the computer
  Serial.print("Distance: ");
  Serial.println(distance);
}
