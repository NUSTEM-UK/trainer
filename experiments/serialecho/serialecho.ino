// Very simple serial echo program.
// For debugging python serial connections

#include <Arduino.h>

void setup() {
    Serial.begin(115200);
}

void loop() {
    while (Serial.available()) {
        Serial.write(Serial.read());
    }
    delay(10);
}
