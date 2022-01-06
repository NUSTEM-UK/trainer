#include <Arduino.h>
#include <SoftwareSerial.h>
#include "ConnectServo.h"

// Serial control setup
#define RX_PIN D2
#define TX_PIN D1
SoftwareSerial myPort(RX_PIN, TX_PIN, false, 256);
bool isSerialZombie = false;

// received characters could be xxx,yyy,zzz,rrr,ggg,bbb,aaa,rrr,ggg,bbb,aaa  or similar
// Let's call it 64 characters, should be loads. Ahem.
char *received = (char *)malloc(sizeof(char) * 64);
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
        Serial.println(F("Invalid SoftwareSerial config"));
        while (1) {
            // Don't continue with invalid config
            delay (1000);
        }
    }
    Serial.println();
    Serial.println(F("SoftwareSerial started"));

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
        // append captured character to received string
        // FIXME: check for overflow
        strcat(received, &incomingChar);
        // received += incomingChar;

        // Check if we have a newline termminator
        if (incomingChar == '\n') {
            // Remove that closing newline from the assembled string
            // received.trim();
            // received[strlen(received) - 1] = '\0';
            // Now parse the received string
            if (strcmp(received, "ACK")) {
                Serial.print(received);
                Serial.println(F(" >>> CEDING CONTROL"));
                myPort.write(ack);
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
                strcpy(received, "");
                Serial.print(F("Received emptied: "));
                Serial.print(received);
                Serial.println(F("See? Gone."));
            } else {
                Serial.println(received);
                Serial.println(F("Missed ACK, reset and try again"));
                // Reset the capture string
                strcpy(received, "");
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

        // FIXME: Check for overflow
        // received += incomingChar;
        strcat(received, &incomingChar);

        // Check if we have a newline termminator
        if (incomingChar == '\n') {
            // Remove that closing newline from the assembled string
            // received.trim();
            received[strlen(received) - 1] = '\0';
            // Now parse the received string
            Serial.print(received);
            Serial.print(": parsed as : ");
            // FIXME: This explodes with a core dump. @WILLNOTFIX
            // I'm going to bail on this effort here, because it's not worth the effort.
            // If I ever need to revisit, pretty sure there's a helpful example here:
            // https://jeffpar.github.io/kbarchive/kb/038/Q38335/
            // ...but for now I'm going to stick with actual String handling,
            // rather than 1980s character arrays. Life is too short.
            sscanf(received, "%03d,%03d", servoD5nextPosition, servoD7nextPosition);
            // servoD5nextPosition = received.substring(0, 3).toInt();
            // servoD7nextPosition = received.substring(4, 7).toInt();
            Serial.print(servoD5nextPosition);
            Serial.print(F(";"));
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
            strcpy(received, "");
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

