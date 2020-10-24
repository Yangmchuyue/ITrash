#include <Servo.h> 

//Arduino Motor PWM Pin Setup
const int topMotorPin = 3;
const int rightMotorPin = 5;
const int botMotorPin = 6;
const int leftMotorPin = 9;

//Motor Signal Input Pins from Rasp Pi Setup
const int pinX = 7;
const int pinZ = 8;

Servo topMotor;
Servo rightMotor;
Servo botMotor;
Servo leftMotor;

int power = 50; //50% power
int signalX;
int signalZ;

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

  //Inputs
  pinMode(pinX, INPUT);
  pinMode(pinZ, INPUT);
}

void loop() {
  //Receiving motor signals from Raspberry Pi
  signalX = digitalRead(pinX);
  signalZ = digitalRead(pinZ);

  //Applying power to motors
  moveX(signalX, power);
  moveZ(signalZ, power);
}


//Functions-------------------------------------------------------------
int moveX(int signal, int power){
  if(signal == 0){
    power = 0;
  }
  topMotor.write(map(power,-100,100,1000,2000));
  botMotor.write(map(-power,-100,100,1000,2000));
}

int moveZ(int signal, int power){
  if(signal == 0){
    power = 0;
  }
  rightMotor.write(map(-power,-100,100,1000,2000));
  leftMotor.write(map(-power,-100,100,1000,2000));
}
