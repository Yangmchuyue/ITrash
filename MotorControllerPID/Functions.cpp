#include "Functions.h"

//PIN SETUP===============================================================
//Ultrasonic Sensor Pins
const int trigPinR = 7; //R for right ultrasonic sensor
const int echoPinR = 8;
const int trigPinB = 12; //B for bottom ultrasonic sensor
const int echoPinB = 13;

//Arduino Motor PWM Pins
const int topMotorPin = 3;
const int rightMotorPin = 5;
const int botMotorPin = 6;
const int leftMotorPin = 9;

Servo topMotor;
Servo rightMotor;
Servo botMotor;
Servo leftMotor;

Functions::Functions(void){}


void Functions::motorSetup(){
    pinMode(topMotorPin, OUTPUT);
    pinMode(rightMotorPin, OUTPUT);
    pinMode(botMotorPin, OUTPUT);
    pinMode(leftMotorPin, OUTPUT);
    topMotor.attach(topMotorPin);
    rightMotor.attach(rightMotorPin);
    botMotor.attach(botMotorPin);
    leftMotor.attach(leftMotorPin);
}

void Functions::ultrasonicSetup(){
    pinMode(trigPinR, OUTPUT);
    pinMode(echoPinR, INPUT);
    pinMode(trigPinB, OUTPUT);
    pinMode(echoPinB, INPUT);
}

void Functions::moveX(double power){
    topMotor.write(map(power, -100, 100, 1000, 2000));
    botMotor.write(map(-power, -100, 100, 1000, 2000));
}

void Functions::moveZ(double power){
    rightMotor.write(map(power, -100, 100, 1000, 2000));
    leftMotor.write(map(power, -100, 100, 1000, 2000));
}

void Functions::moveToPositionX(double targetX, double distanceX, double power){
    double margin = 3.0;
    double error = distanceX - targetX;
    if (abs(error) > margin) { //check if robot is close enough to target position
        if (error > 0) moveX(power);
        else moveX(-power);
    }
    else moveX(0);
}

void Functions::moveToPositionZ(double targetZ, double distanceZ, double power){
    double margin = 5.0;
    double error = distanceZ - targetZ;
    if (abs(error) > margin) { //check if robot is close enough to target position
        if (error > 0) moveZ(power);
        else moveZ(-power);
    }
    else moveZ(0);
}

double Functions::ultrasonicDist(int trigPin, int echoPin){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    double duration = pulseIn(echoPin, HIGH);
    return (0.034 * duration) / 2;
}

