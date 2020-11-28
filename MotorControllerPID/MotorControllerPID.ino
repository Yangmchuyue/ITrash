/*
 * Library: https://playground.arduino.cc/Code/PIDLibrary/
 */

#include "Functions.h"


//VARIABLES======================================================================
//Motion
double outputX, outputZ;
double distanceX, distanceZ;
double targetX, targetZ;
double prevDistX = 0, prevDistZ = 0;
double minDist = 15.0, maxDist = 150.0;
double errorX = 0, errorZ = 0;
//PID
//P controller -> xKP = 5.1
//Tu = 0.91 Ku = 8.5
#define XKI 1.5
#define ZKI 1.5
// 5.4 (5 at full battery), 1.5, 0.1
double xKp = 5, xKi = XKI, xKd = 0.1;
double zKp = 5, zKi = ZKI, zKd = 0.1;

//Communication:
int index;
String data, xData, zData;
String displayOutput;
bool pause = true;

int counter = 0;

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
    prevDistX = functions.ultrasonicDist(trigPinR, echoPinR); 
    prevDistZ = functions.ultrasonicDist(trigPinB, echoPinB); 
    functions.pidOff(&xPID, &zPID);
    xPID.SetOutputLimits(-90, 90);
    zPID.SetOutputLimits(-90, 90);
}


//MAIN FUNCTION===================================================================
void loop(){
    //Collecting Sensor Data
    distanceX = functions.ultrasonicDist(trigPinR, echoPinR); 
    distanceZ = functions.ultrasonicDist(trigPinB, echoPinB);
    //If the value changes by over 30 cm in one iteration of this loop, ignore this reading
    if (abs(distanceX - prevDistX) > 30) distanceX = prevDistX;
    if (abs(distanceZ - prevDistZ) > 30) distanceZ = prevDistZ;
    prevDistX = distanceX;
    prevDistZ = distanceZ;
    errorX = targetX - distanceX;
    errorZ = targetZ - distanceZ;

    //Receiving commands from Raspberry Pi
    if (Serial.available() > 0){
        functions.pidOff(&xPID, &zPID);
        data = Serial.readStringUntil('\n');
        if (data == "q" || data == "" || data == " "){
            pause = true;
        }
        else{
            functions.processData(data, &targetX, &targetZ, minDist, maxDist);
            pause = false;
        }
    }
    
    //Moving the robot
    if (!pause){
        //Turn PID on and compute the output
        xPID.SetMode(AUTOMATIC);
        zPID.SetMode(AUTOMATIC);
        xKi = 0;
        if (abs(outputX) < 50) xKi = XKI; //Only start calculating integral component when robot is slowing down
        xPID.Compute();
        functions.moveX((int)outputX);

        //Checking if robot is steady at target
        if (counter > 20){  //after 20 * 50 ms = 1 s within 10 cm of target position, stop the robot
            pause = true;
            counter = 0;
        }
        if (abs(errorX) < 10) counter++;
        else counter = 0;

        //Displaying sensor values and target position
        displayOutput = "X:" + String(distanceX) + "  Z:" + String(distanceZ);
        displayOutput += "  (" + String(targetX) + "," + String(targetZ) + ")";
        displayOutput += "  Power: " + String(outputX);
        Serial.println(displayOutput);
    }
    else{
        functions.pidOff(&xPID, &zPID);
    }

    delay(50);
}



