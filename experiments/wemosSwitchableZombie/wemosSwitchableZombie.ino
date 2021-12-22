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

    // Check if we have a character incoming
    if (myPort.available() > 0) {
        // Read incoming, and append to capture string
        incomingChar = myPort.read();
        received += incomingChar;

        // Check if we have a newline terminator
        if (incomingChar == '\n') {
            // Remove that closing newline from the assembled string
            received.trim();
            // Now parse the received string
            if (received == "ACK") {
                Serial.print(received);
                Serial.println(" >>> CEDING CONTROL");
                isSerialZombie = true;
                myPort.write(ack);
                // for (int i = 0; i < 10; i++) {
                //     myPort.write(i);
                //     delay(250);
                // }
            } else {
                Serial.println(received);
            }
            // Reset the capture string
            received = "";
        }
    }
}
