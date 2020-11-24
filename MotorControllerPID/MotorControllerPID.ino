/*
 * Library: https://playground.arduino.cc/Code/PIDLibrary/
 */

#include "Functions.h"
#include <PID_v1.h>


//VARIABLES======================================================================
//Motion
double outputX, outputZ;
double distanceX, distanceZ;
double minDist = 8.0, maxDist = 250.0;
double targetX, targetZ;
//Tu = 0.96 Ku = 11
double xKp = 6, xKi = 15, xKd = 0.8; //6, 13, 0.8
double zKp = 5, zKi = 15, zKd = 0.8;
double errorX, errorZ;

//Communication:
int index;
String data, xData, zData;
String displayOutput;
bool pause = true;


//OBJECTS========================================================================
Functions functions;
PID xPID(&distanceX, &outputX, &targetX, xKp, xKi, xKd, P_ON_E, DIRECT);
PID zPID(&distanceZ, &outputZ, &targetZ, zKp, zKi, zKd, P_ON_E, DIRECT);


//SETUP==========================================================================
void setup(){
    Serial.begin(9600);
    functions.motorSetup();
    functions.ultrasonicSetup();
    //Initialize targets to 20.0 cm
    targetX = 20.0;
    targetZ = 20.0;
    //Set the PID to off at start
    xPID.SetMode(MANUAL);
    zPID.SetMode(MANUAL);
    //xPID.SetControllerDirection(REVERSE);
    //zPID.SetControllerDirection(REVERSE);
    xPID.SetOutputLimits(-90, 90);
    zPID.SetOutputLimits(-90, 90);
}


//MAIN FUNCTION===================================================================
void loop(){
    //Collecting Sensor Data
    distanceX = functions.ultrasonicDist(trigPinR, echoPinR); //Right Ultrasonic Sensor
    distanceZ = functions.ultrasonicDist(trigPinB, echoPinB); //Bottom Ultrasonic Sensor
    errorX = targetX - distanceX;
    errorZ = targetZ - distanceZ;
    
    //Receiving commands from Raspberry Pi
    if (Serial.available() > 0){
        data = Serial.readStringUntil('\n');
        if (data == "q"){
            pause = true;
            xPID.SetMode(MANUAL);
            zPID.SetMode(MANUAL);
            functions.moveX(0);
            functions.moveZ(0);
        }
        else if (data == "" || data == " "){ //If user enters in nothing, the robot pauses
            if (pause) pause = false;
            else pause = true;
        }
        else{
            pause = false;
            index = data.indexOf(" ");
            xData = data.substring(0,index);
            zData = data.substring(index+1);
            targetX = xData.toFloat();
            targetZ = zData.toFloat();
            functions.filterData(&targetX, &targetZ, minDist, maxDist);
            xPID.SetMode(MANUAL);
            zPID.SetMode(MANUAL);
        }
    }
    
    //Moving the robot
    if (!pause){
        //Turn PID on and compute the output
        xPID.SetMode(AUTOMATIC);
        zPID.SetMode(AUTOMATIC);
        xKi = 0;
        zKi = 0;
        if (abs(errorX) < 15.0) xKi = 15;
        if (abs(errorZ) < 15.0) zKi = 15;
        xPID.Compute();
        zPID.Compute();
        functions.moveX((int)outputX);
        //functions.moveZ((int)outputZ);

        //Displaying sensor values and target position
        displayOutput = "X:" + String(distanceX) + "  Z:" + String(distanceZ);
        displayOutput += "  (" + String(targetX) + "," + String(targetZ) + ")";
        Serial.println(displayOutput);
    }
    else{
        //Turn PID and motors off
        xPID.SetMode(MANUAL);
        zPID.SetMode(MANUAL);
        functions.moveX(0);
        functions.moveZ(0);
    }
    delay(50);
}



