/**
 * The big brain tells microcontroller exact movements through Serial.
 * For all commands INCLUDING 0, sends additional 0 byte when done.
 *
 * (x) means you fill this in.
 * (x) is 1 byte unsigned
 * (2x) is 2 bytes unsigned big endian
 *
 * Available commands:
 * 0(x) : Echo byte (x)
 * 1(x) : Set servo to angle (x) (0-180)
 * 2(i) : Turn off stepper (i) (0 or 1)
 * 3(i) : Turn on stepper (i) (0 or 1)
 * 4(i)(d)(2s)(2t) : Move stepper (i) direction (d), (s) steps, (t) us per step.
*/

#include <Servo.h>

constexpr int SERVO_OFFSET = 22;


uint16_t read16() {
    uint16_t val = Serial.read();
    val = (val << 8) | Serial.read();
    return val;
}


void setup() {
    Serial.begin(9600);

    Servo servo;
    int servo_pos = SERVO_OFFSET;
    servo.attach(8);
    servo.write(SERVO_OFFSET);

    pinMode(LED_BUILTIN, OUTPUT);
    for (int i = 2; i <= 7; i++) {
        pinMode(i, OUTPUT);
    }

    while (true) {
        digitalWrite(LED_BUILTIN, HIGH);
        while (Serial.available() == 0);
        digitalWrite(LED_BUILTIN, LOW);

        // Get one byte to determine command
        int command = Serial.read();
        // Get required bytes.
        int req = 0;
        switch (command) {
            case 0: req = 1; break;
            case 1: req = 1; break;
            case 2: req = 1; break;
            case 3: req = 1; break;
            case 4: req = 6; break;
        }
        while (Serial.available() < req);

        // Execute command
        if (command == 0) {
            Serial.write(Serial.read());
        } else if (command == 1) {
            int target = Serial.read() + SERVO_OFFSET;
            int delta = (target > servo_pos) ? 1 : -1;
            for (int i = servo_pos; i != target; i += delta) {
                servo.write(i);
                delay(10);
            }
            servo_pos = target;

            // Stop servo for a moment to prevent vibration
            delay(200);
            servo.detach();
            delay(300);
            servo.attach(8);
        } else if (command <= 4) {
            int id = Serial.read();
            int pin_offset = 3*id + 2;

            if (command <= 3) {
                digitalWrite(pin_offset, command == 2);
            } else {
                int dir = Serial.read();
                int steps = read16();
                int time = read16();

                digitalWrite(pin_offset + 1, dir);
                for (int i = 0; i < steps; i++) {
                    digitalWrite(pin_offset + 2, HIGH);
                    digitalWrite(pin_offset + 2, LOW);
                    delayMicroseconds(time);
                }
            }
        } else {
            continue;
        }

        Serial.write(0);
        Serial.flush();
    }
}

void loop() {
}
