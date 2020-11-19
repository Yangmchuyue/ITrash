/*
 * Library: https://playground.arduino.cc/Code/PIDLibrary/
 */

#include "Functions.h"
#include <PID_v1.h>


//VARIABLES======================================================================
//Motion
double outputX, outputZ;
double distanceX, distanceZ;
double targetX, targetZ;
double xKp = 0, xKi = 0, xKd = 0;
double zKp = 0, zKi = 0, zKd = 0;

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
    xPID.SetOutputLimits(-100, 100);
    zPID.SetOutputLimits(-100, 100);
}


//MAIN FUNCTION===================================================================
void loop(){
    //Collecting Sensor Data
    distanceX = functions.ultrasonicDist(trigPinR, echoPinR); //Right Ultrasonic Sensor
    distanceZ = functions.ultrasonicDist(trigPinB, echoPinB); //Bottom Ultrasonic Sensor

    //Receiving commands from Raspberry Pi
    if (Serial.available() > 0){
        data = Serial.readStringUntil('\n');
        if (data == "q"){
            pause = true;
        }
        else if (data == ""){ //If user enters in nothing, the robot pauses
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
        }
    }
    
    //Moving the robot
    if (!pause){
        //Turn PID on and compute the output
        xPID.SetMode(AUTOMATIC);
        zPID.SetMode(AUTOMATIC);
        xPID.Compute();
        zPID.Compute();
        functions.moveX(outputX);
        functions.moveZ(outputZ);
    }
    else{
        //Turn PID and motors off
        xPID.SetMode(MANUAL);
        zPID.SetMode(MANUAL);
        functions.moveX(0);
        functions.moveZ(0);
    }
    
    //Displaying sensor values and target position
    displayOutput = "X:" + String(distanceX) + " Z:" + String(distanceZ) + " (" + String(targetX) + "," + String(targetZ) + ")";
    Serial.println(displayOutput);
    delay(50);
}



