#include <Arduino.h>
#include <SoftwareSerial.h>
#include "ConnectServo.h"

// Serial control setup
#define RX_PIN D2
#define TX_PIN D1
SoftwareSerial myPort(RX_PIN, TX_PIN, false, 256);
bool isSerialZombie = false;
String received;
char incomingChar = 0;

const char *ack = "ACK ACK ACK";

// Connect Servo setup
ConnectServo servoD5;
ConnectServo servoD7;
extern ServoMessenger ConnectMessenger;
// Set pins for servos
static const uint8_t servoD5Pin = D5;
static const uint8_t servoD7Pin = D7;
uint8_t servoD5nextPosition = 0;
uint8_t servoD7nextPosition = 0;


void setup() {
    Serial.begin(115200); // Standard hardware serial port, for debugging
    myPort.begin(9600);
    // myPort.begin(9600, SWSERIAL_8N1, D6, D6, false, 256);
    if (!myPort) {
        Serial.println("Invalid SoftwareSerial config");
        while (1) {
            // Don't continue with invalid config
            delay (1000);
        }
    }
    Serial.println();
    Serial.println("SoftwareSerial started");

    servoD5.setPin(servoD5Pin);
    servoD7.setPin(servoD7Pin);

    delay(500);
}

void loop() {

    // Update the servos anyway, they'll run out their queues.
    ConnectMessenger.updateServos();

    if (!isSerialZombie) {
        goAboutYourBusiness();
        checkSerialConnection();
    } else {
        parseSerialCommandsAndDriveServos();
    }


}

void checkSerialConnection() {
    if (myPort.available() > 0) {
        // read incoming. append to capture string
        incomingChar = myPort.read();
        received += incomingChar;

        // Check if we have a newline termminator
        if (incomingChar == '\n') {
            // Remove that closing newline from the assembled string
            received.trim();
            // Now parse the received string
            if (received == "ACK") {
                Serial.print(received);
                Serial.println(" >>> CEDING CONTROL");
                myPort.write(ack);
                // Let the world know we're a zombie
                isSerialZombie = true;
                // Short delay to give servos time to run out a bit
                delay(500);
                received = "";
            } else {
                Serial.println(received);
                Serial.println("We missed the ACK");
                // Reset the capture string
                received = "";
            }
        }
    }
}

void parseSerialCommandsAndDriveServos() {
    Serial.println("We're a zombie");
    delay(1000);

    // // Reset the capture string
    // received += incomingChar;
    // // Get commands
    // if (myPort.available() > 0) {
    //     // read incoming. append to capture string
    //     incomingChar = myPort.read();

    //     // Check if we have a newline termminator
    //     if (incomingChar == '\n') {
    //         // Remove that closing newline from the assembled string
    //         received.trim();
    //         // Now parse the received string
    //         Serial.println(received);
    //         // Reset the capture string
    //         // Let the world know we're a zombie
    //         return;
    //     }
    // }
}

void goAboutYourBusiness() {
    // Standard ConnectServo stuff
    // Check if servoD5 has stopped
    if (!servoD5.isMovingAndCallYield()) {
        // Set servo moving again, at random speed
        servoD5.queueEaseTo(servoD5nextPosition, EASE_CUBIC_IN_OUT, random(20, 150));
        // Flip end position
        servoD5nextPosition = 180-servoD5nextPosition;
    }
    // Check if servoD7 has stopped
    if (!servoD7.isMovingAndCallYield()) {
        // Set servo moving again, at random speed
        servoD7.queueEaseTo(servoD7nextPosition, EASE_CUBIC_IN_OUT, random(20, 150));
        // Flip end position
        servoD7nextPosition = 180-servoD7nextPosition;
    }
}

