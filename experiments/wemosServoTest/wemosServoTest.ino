#include <Arduino.h>
#include <SoftwareSerial.h>
#include "ConnectServo.h"

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

// Serial control setup
#define RX_PIN D2
#define TX_PIN D1
SoftwareSerial myPort(RX_PIN, TX_PIN, false, 256);
bool isSerialZombie = false;
String received;
char incomingChar = 0;

const char *ack = "ACK ACK ACK";

void setup() {
    Serial.begin(115200); // Standard hardware serial port, for debugging
    Serial.println();
    myPort.begin(57600);
    // myPort.begin(9600, SWSERIAL_8N1, D6, D6, false, 256);
    if (!myPort) {
        Serial.println("Invalid SoftwareSerial config");
        while (1) {
            // Don't continue with invalid config
            delay (1000);
        }
    }
    servoD5.setPin(servoD5Pin);
    servoD7.setPin(servoD7Pin);


    delay(500);
    myPort.write(ack);
}

void loop() {
    // for (uint8_t i = 0; i < 180; i++) {
    //     servoD5.write(i);
    //     servoD7.write(180-i);
    //     // servoD5.write(servoD5nextPosition);
    //     // servoD7.write(servoD7nextPosition);
    //     delay(10);
    //     parseSerialCommandsAndDriveServos();
    // }
    // for (uint8_t i = 180; i > 0; i--) {
    //     servoD5.write(i);
    //     servoD7.write(180-i);
    //     // servoD5.write(servoD5nextPosition);
    //     // servoD7.write(servoD7nextPosition);
    //     delay(10);
    //     parseSerialCommandsAndDriveServos();
    // }
    parseSerialCommandsAndDriveServos();
    if (servoD5nextPosition != servoD5currentPosition) {
        servoD5.write(servoD5nextPosition);
        servoD5currentPosition = servoD5nextPosition;
    }
    if (servoD7nextPosition != servoD7currentPosition) {
        servoD7.write(servoD7nextPosition);
        servoD7currentPosition = servoD7nextPosition;
    }
    delay(10);

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

            // Move the servos!
            // servoD5.queueMoveTo(servoD5nextPosition);
            // servoD7.queueMoveTo(servoD7nextPosition);
            // servoD5.attach(D5);
            // servoD7.attach(D7);
            // servoD5.write(servoD5nextPosition);
            // servoD7.write(servoD7nextPosition);
            // delay(50);

            // Reset the capture string
            received = "";

        }
    }
}
