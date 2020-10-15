#include <Servo.h>

//Setting the Arduino pwm (pulse-width-modulation) pins for each motor.
int motor1Pin = 3;
int motor2Pin = 5;
int motor3Pin = 6;
int motor4Pin = 9;

//Creating Servo objects for each motor.
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;

void setup() {
  // put your setup code here, to run once:
  pinMode(motor1Pin,OUTPUT);
  pinMode(motor2Pin,OUTPUT);
  pinMode(motor3Pin,OUTPUT);
  pinMode(motor4Pin,OUTPUT);
  
  motor1.attach(motor1Pin);
  motor2.attach(motor2Pin);
  motor3.attach(motor3Pin);
  motor4.attach(motor4Pin);
}

void loop() {
  // put your main code here, to run repeatedly:
  move(30); //move motors forward at 30% power
  delay(1000);
  move(-30); //move motors backward at 30% power
  delay(1000);
}

int move(int value){
  /*These map functions convert an input between -100 (max power backwards) and 100 (max power forwards)
   *into a number (between 1000 and 2000) that the motor reads.
  */
  motor1.write(map(value,-100,100,1000,2000));
  motor2.write(map(value,-100,100,1000,2000));
  motor3.write(map(value,-100,100,1000,2000));
  motor4.write(map(value,-100,100,1000,2000));
}



