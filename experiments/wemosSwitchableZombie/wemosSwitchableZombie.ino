#include <Arduino.h>
#include <SoftwareSerial.h>
#include "ConnectServo.h"

// Serial control setup
// Wemos D1
// #define RX_PIN D2
// #define TX_PIN D1
// Kniwwelino
#define RX_PIN D6
#define TX_PIN D0
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
uint8_t servoD5currentPosition = 0;
uint8_t servoD7currentPosition = 0;


void setup() {
    Serial.begin(115200); // Standard hardware serial port, for debugging
    myPort.begin(57600);  // Doesn't seem to be an issue with faster baud rates
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

    if (!isSerialZombie) {
        // Update the servos anyway, they'll run out their queues.
        ConnectMessenger.updateServos();
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
                delay(100);
                // myPort.write(ack);
                myPort.write("ACK ACK ACK");
                Serial.println(ack);

                // Let the world know we're a zombie
                isSerialZombie = true;
                // servoD5.detach();
                // servoD7.detach();
                // Make sure the servos don't time out on us.
                // servoD5.keepActive();
                // servoD7.keepActive();
                // Short delay to give servos time to run out a bit
                delay(500);
                // Clear the capture string
                // Can't do this at the top of the function since we may not
                // grab the whole command in one pass.
                received = "";
            } else {
                Serial.println(received);
                Serial.println("Missed ACK, reset and try again");
                // Reset the capture string
                received = "";
            }
        }
    }
}

void parseSerialCommandsAndDriveServos() {
    // Serial.println("We're a zombie");
    // TODO: Empty servo queues here
    //       Needs handler in ConnectMessenger
    // delay(1000);

    // Get commands
    if (myPort.available() > 0) {
        // read incoming. append to capture string
        incomingChar = myPort.read();
        // FIXME: Replace received with a char array here, shouldn't
        //        really be using Strings for this, it can blow up badly.
        //        See discussion of sscanf() here:
        //        https://forum.arduino.cc/t/arduino-sscanf/309063/6
        received += incomingChar;

        // Check if we have a newline termminator
        if (incomingChar == '\n') {
            // Remove that closing newline from the assembled string
            received.trim();
            // Now parse the received string
            Serial.print(received);
            Serial.print(": parsed as : ");
            servoD5nextPosition = received.substring(0, 3).toInt();
            servoD7nextPosition = received.substring(4, 7).toInt();
            Serial.print(servoD5nextPosition);
            Serial.print(";");
            Serial.println(servoD7nextPosition);

            // Move the servos, if they need moving
            // (check needed to avoid jitter and stallout from repeatedly
            // writing the same destination to a servo, which apparently is Bad)
            if (servoD5nextPosition != servoD5currentPosition) {
                servoD5.write(servoD5nextPosition);
                servoD5currentPosition = servoD5nextPosition;
            }
            if (servoD7nextPosition != servoD7currentPosition) {
                servoD7.write(servoD7nextPosition);
                servoD7currentPosition = servoD7nextPosition;
            }
            delay(10);

            // Reset the capture string
            received = "";

        }
    }
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

