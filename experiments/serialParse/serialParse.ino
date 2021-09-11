#include <Arduino.h

String x;
int i;

void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);
}

void loop() {
    while (!Serial.available()) {
        x = Serial.readString();
        Serial.println(x);
        if (x == "cabbage") {
            Serial.println("...is horrid");
            Serial.println(i++);
        }
    }
}
