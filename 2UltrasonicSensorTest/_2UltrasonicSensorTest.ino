const int trigPinR = 7; //R for right ultrasonic sensor
const int echoPinR = 8;
const int trigPinB = 12; //B for bottom ultrasonic sensor
const int echoPinB = 13;

long durationR; 
long durationB; 
long distanceR;
long distanceB; 

void setup() {
  Serial.begin(9600); 
  pinMode(trigPinR, OUTPUT); 
  pinMode(echoPinR, INPUT);  
  pinMode(trigPinB, OUTPUT);
  pinMode(echoPinB, INPUT);
}

void loop() {
  //We can not run the sensors synchronuously, as the signals will interfere with eachother. Instead, we can have the sensors alternate.
  
  //Right Ultrasonic Sensor
  digitalWrite(trigPinR, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinR, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinR, LOW);

  durationR = pulseIn(echoPinR, HIGH);
  distanceR = (0.034*durationR)/2;

  //Bottom Ultrasonic Sensor
  digitalWrite(trigPinB, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinB, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinB, LOW);

  durationB = pulseIn(echoPinB, HIGH);
  distanceB = (0.034*durationB)/2;
  
  //Printing the distance on the computer
  Serial.print("Distance from right: ");
  Serial.print(distanceR);
  Serial.print("   Distance from bottom: ");
  Serial.println(distanceB);
}
