// Working as of 2021-12-21, with picoserial.py test script.

#include <Arduino.h>
#include <SoftwareSerial.h>

#define RX_PIN D2
#define TX_PIN D1
SoftwareSerial myPort(RX_PIN, TX_PIN, false, 256);

String received;
char incomingChar = 0;

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
    delay(500);

}

void loop() {
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
            if (received == "cabbage") {
                Serial.print(received);
                Serial.println("...is horrid");
            } else {
                Serial.println(received);
            }
            // Reset the capture string
            received = "";
        }
    }
}
