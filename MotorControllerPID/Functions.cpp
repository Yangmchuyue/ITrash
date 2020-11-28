#include "Functions.h"

//PIN SETUP===============================================================
//Ultrasonic Sensor Pins
const int trigPinB = 7; //B for bottom ultrasonic sensor
const int echoPinB = 8;
const int trigPinR = 12; //R for right ultrasonic sensor
const int echoPinR = 13;

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

void Functions::processData(String data, double *targetX, double *targetZ, int minDist, int maxDist){
    int index = data.indexOf(" ");
    *targetX = data.substring(0,index).toFloat();
    *targetZ = data.substring(index+1).toFloat();
    if (*targetX < minDist) *targetX = minDist;
    if (*targetZ < minDist) *targetZ = minDist;
    if (*targetX > maxDist) *targetX = maxDist;
    if (*targetZ > maxDist) *targetZ = maxDist;
}

void Functions::filterData(double *targetX, double *targetZ, int minDist, int maxDist){
    if (*targetX < minDist) *targetX = minDist;
    if (*targetZ < minDist) *targetZ = minDist;
    if (*targetX > maxDist) *targetX = maxDist;
    if (*targetZ > maxDist) *targetZ = maxDist;
}

void Functions::moveX(int power){
    topMotor.write(map(-power, -100, 100, 1000, 2000));
    botMotor.write(map(power, -100, 100, 1000, 2000));
}

void Functions::moveZ(int power){
    rightMotor.write(map(-power, -100, 100, 1000, 2000));
    leftMotor.write(map(-power, -100, 100, 1000, 2000));
}

void Functions::moveToPositionX(double targetX, double distanceX, int power){
    double margin = 3.0;
    double error = targetX - distanceX;
    if (abs(error) > margin) { //check if robot is close enough to target position
        if (error > 0) moveX(power);
        else moveX(-power);
    }
    else moveX(0);
}

void Functions::moveToPositionZ(double targetZ, double distanceZ, int power){
    double margin = 5.0;
    double error = targetZ - distanceZ;
    if (abs(error) > margin) { //check if robot is close enough to target position
        if (error > 0) moveZ(power);
        else moveZ(-power);
    }
    else moveZ(0);
}

void Functions::pidOff(PID *xPID, PID *zPID){
    xPID->SetMode(MANUAL);
    zPID->SetMode(MANUAL);
    Functions::moveX(0);
    Functions::moveZ(0);
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


