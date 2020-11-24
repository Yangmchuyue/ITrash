/*
 * MotorController.h - header file for declaring functions
 */

#ifndef Functions_h
#define Functions_h

#include "Arduino.h"
#include <Servo.h>


//PIN SETUP===============================================================
//Ultrasonic Sensor Pins
extern const int trigPinR; //R for right ultrasonic sensor
extern const int echoPinR;
extern const int trigPinB; //B for bottom ultrasonic sensor
extern const int echoPinB;

//Arduino Motor PWM Pins
extern const int topMotorPin;
extern const int rightMotorPin;
extern const int botMotorPin;
extern const int leftMotorPin;

extern Servo topMotor;
extern Servo rightMotor;
extern Servo botMotor;
extern Servo leftMotor;


class Functions {
    public:
        //Constructor
        Functions(void);
        
        //Methods
        void motorSetup();
        void ultrasonicSetup();
        void filterData(double *targetX, double *targetZ, int minDist, int maxDist);
        void moveX(int power);
        void moveZ(int power);
        void moveToPositionX(double targetX, double distanceX, int power);
        void moveToPositionZ(double targetZ, double distanceZ, int power);
        double ultrasonicDist(int trigPin, int echoPin);
        
    private:
    
};

#endif

