#include <Arduino.h>
#include <SoftwareSerial.h>

#define RX_PIN D2
#define TX_PIN D1
SoftwareSerial myPort(RX_PIN, TX_PIN, false, 256);

String x;
int incomingByte = 0;
int i;

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
    if (myPort.available() > 0) {
        // x = myPort.readString();
        incomingByte = myPort.read();
        Serial.println(incomingByte, DEC);
        // if (x == "cabbage") {
        //     Serial.println("...is horrid");
        //     Serial.println(i++);
    }
}
