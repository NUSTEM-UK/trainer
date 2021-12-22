#include <Arduino.h>
#include <SoftwareSerial.h>

// Serial control setup
#define RX_PIN D2
#define TX_PIN D1
SoftwareSerial myPort(RX_PIN, TX_PIN, false, 256);
bool isSerialZombie = false;
String received;
char incomingChar = 0;
char buf[8];

const char *gash1 = "Hello, world!";
const char *gash2 = "80";


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

    // if (!isSerialZombie) {
    //     Serial.println("Not a zombie");
    //     delay(1000);
    // }

    // for (int i = 65; i < 91; i++) {
    //     itoa(i, buf, 10);
    //     myPort.write(buf);
    //     // myPort.write('\n');
    //     Serial.println(i);
    //     delay(250);
    // }


    myPort.write(gash1);
    Serial.println(gash1);
    delay(1000);
    myPort.write(gash2);
    Serial.println(gash2);
    delay(1000);



    // // Check if we have a character incoming
    // if (myPort.available() > 0) {
    //     // Read incoming, and append to capture string
    //     incomingChar = myPort.read();
    //     received += incomingChar;

    //     // Check if we have a newline terminator
    //     if (incomingChar == '\n') {
    //         // Remove that closing newline from the assembled string
    //         received.trim();
    //         // Now parse the received string
    //         if (received == "ACK") {
    //             Serial.print(received);
    //             Serial.println(" >>> CEDING CONTROL");
    //             isSerialZombie = true;
    //             myPort.write('ACK ACK ACK\n');
    //         } else {
    //             Serial.println(received);
    //         }
    //         // Reset the capture string
    //         received = "";
    //     }
    // }
}
