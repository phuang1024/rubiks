/**
 * The big brain tells microcontroller exact movements through Serial.
 * For all commands INCLUDING 0, sends additional 0 byte when done.
 * Available commands:
 * 0(x) : Echo byte (x)
 * 1(x) : Set servo to angle (x) (0-180)
 * 2(i) : Turn off stepper (i) (0 or 1)
 * 3(i) : Turn on stepper (i) (0 or 1)
 * 4(i)(d)(s)(t) : Move stepper (i) direction (d), (s) steps, (t) us per step.
*/

#include <Servo.h>

constexpr int SERVO_OFFSET = 0;


void setup() {
    Servo servo;
    servo.attach(8);
    servo.write(SERVO_OFFSET);

    while (true) {
        while (Serial.available() == 0);

        // Get one byte to determine command
        int command = Serial.read();
        // Get required bytes.
        int req = 0;
        switch (command) {
            case 0: req = 1; break;
            case 1: req = 1; break;
            case 2: req = 1; break;
            case 3: req = 1; break;
            case 4: req = 4; break;
        }
        while (Serial.available() < req);

        // Execute command
        if (command == 0) {
            Serial.write(Serial.read());
        } else if (command == 1) {
            servo.write(Serial.read() + SERVO_OFFSET);
            // Just guessing that it takes this long.
            delay(200);
        } else if (command <= 4) {
            int id = Serial.read();
            int pin_offset = 3*id + 2;

            if (command <= 3) {
                digitalWrite(pin_offset, command == 2);
            } else {
                int dir = Serial.read();
                int steps = Serial.read();
                int time = Serial.read();

                digitalWrite(pin_offset + 1, dir);
                for (int i = 0; i < steps; i++) {
                    digitalWrite(pin_offset + 2, HIGH);
                    digitalWrite(pin_offset + 2, LOW);
                    delayMicroseconds(time);
                }
            }
        }

        Serial.write(0);
        Serial.flush();
    }
}

void loop() {
}
