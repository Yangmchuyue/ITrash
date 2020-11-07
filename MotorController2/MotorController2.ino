#include <Servo.h>

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

//FUNCTIONS===============================================================
void moveX(int power){
    topMotor.write(map(power, -100, 100, 1000, 2000));
    botMotor.write(map(-power, -100, 100, 1000, 2000));
}

void moveZ(int power){
    rightMotor.write(map(power, -100, 100, 1000, 2000));
    leftMotor.write(map(power, -100, 100, 1000, 2000));
}

void moveToPositionX(long targetX, long distanceX, int power){
    long margin = 3.0;
    long error = distanceX - targetX;
    if (abs(error) > margin) { //check if robot is close enough to target position
        if (error > 0) {
            moveX(power);
        }
        else {
            moveX(-power);
        }
    }
    else {
        moveX(0);
    }
}

void moveToPositionZ(long targetZ, long distanceZ, int power){
    long margin = 5.0;
    long error = distanceZ - targetZ;
    if (abs(error) > margin) { //check if robot is close enough to target position
        if (error > 0) {
            moveZ(power);
        }
        else {
            moveZ(-power);
        }
    }
    else {
        moveZ(0);
    }
}

long ultrasonicDist(int trigPin, int echoPin){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH);
    return (0.034 * duration) / 2;
}

//VARIABLES======================================================================
long distanceX;
long distanceZ;
long targetX = 20.0;
long targetZ = 20.0;
int power = 30;
int index;
String data, xData, zData;
String displayOutput;
bool pause = true;

//SETUP==========================================================================
void setup(){
    Serial.begin(9600);
    //Motors
    pinMode(topMotorPin, OUTPUT);
    pinMode(rightMotorPin, OUTPUT);
    pinMode(botMotorPin, OUTPUT);
    pinMode(leftMotorPin, OUTPUT);
    topMotor.attach(topMotorPin);
    rightMotor.attach(rightMotorPin);
    botMotor.attach(botMotorPin);
    leftMotor.attach(leftMotorPin);
    //Ultrasonic Sensors
    pinMode(trigPinR, OUTPUT);
    pinMode(echoPinR, INPUT);
    pinMode(trigPinB, OUTPUT);
    pinMode(echoPinB, INPUT);
}

//MAIN FUNCTION===================================================================
void loop(){
    distanceX = ultrasonicDist(trigPinR, echoPinR); //Right Ultrasonic Sensor
    distanceZ = ultrasonicDist(trigPinB, echoPinB); //Bottom Ultrasonic Sensor
    
    //Receiving commands from Raspberry Pi
    if (Serial.available() > 0){
        data = Serial.readStringUntil('\n');
        if (data == "q"){
            pause = true;
        }
        else if (data == ""){ //If user enters in nothing, the robot pauses
            if (pause){
                pause = false;
            }
            else{
                pause = true;
            } 
        }
        else{
            pause = false;
            index = data.indexOf(" ");
            xData = data.substring(0,index);
            zData = data.substring(index+1);
            targetX = xData.toFloat();
            targetZ = zData.toFloat();
        }
    }
    
    //Moving the robot
    if (!pause){
        moveToPositionX(targetX, distanceX, power);
        moveToPositionZ(targetZ, distanceZ, power);
    }
    else{
        moveX(0);
        moveZ(0);
    }
    
    //Displaying sensor values and target position
    displayOutput = "X:" + String(distanceX) + " Z:" + String(distanceZ) + " (" + String(targetX) + "," + String(targetZ) + ")";
    Serial.println(displayOutput);
    delay(50);
}



