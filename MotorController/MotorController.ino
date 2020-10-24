#include <Servo.h> 

//Arduino Motor PWM Pin Setup
const int topMotorPin = 3;
const int rightMotorPin = 5;
const int botMotorPin = 6;
const int leftMotorPin = 9;

//Ultrasonic Sensor Input Pins from Rasp Pi Setup
const int rightUltrasonicPin = 7;
const int botUltrasonicPin = 8;

int rightDistance;
int botDistance;

Servo topMotor;
Servo rightMotor;
Servo botMotor;
Servo leftMotor;

void setup() {
  Serial.begin(9600);
  
  //Motors
  pinMode(topMotorPin,OUTPUT);
  pinMode(rightMotorPin,OUTPUT);
  pinMode(botMotorPin,OUTPUT);
  pinMode(leftMotorPin,OUTPUT);
  
  topMotor.attach(topMotorPin);
  rightMotor.attach(rightMotorPin);
  botMotor.attach(botMotorPin);
  leftMotor.attach(leftMotorPin);

  //Sensors 
  pinMode(rightUltrasonicPin, INPUT);
  pinMode(botUltrasonicPin, INPUT);
}

void loop() {
  //Receiving ultrasonic sensor data from Raspberry Pi
  rightDistance = digitalRead(rightUltrasonicPin);
  botDistance = digitalRead(botUltrasonicPin);
}

//Functions-------------------------------------------------------------
int moveVertical(int value){
  rightMotor.write(map(-value,-100,100,1000,2000));
  leftMotor.write(map(-value,-100,100,1000,2000));
}

int moveHorizontal(int value){
  topMotor.write(map(value,-100,100,1000,2000));
  botMotor.write(map(-value,-100,100,1000,2000));
}
