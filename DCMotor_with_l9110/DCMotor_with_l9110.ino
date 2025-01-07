#include <Arduino.h>


// Motor control pins
const int A1 = 1;  // Motor input pin 1
const int A2 = 4;  // Motor input pin 2

// Motor control variables
int motorSpeed = 120;     // Speed (0 to 255)
bool direction = true;  // true for forward, false for backward

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(115200);

  // Set motor control pins as outputs
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);


  // Start in a stopped state
  stopMotor();
}

void loop() {
  // Read commands from the Serial Monitor for testing
  if (Serial.available()) {
    char command = Serial.read();
    Serial.println(command);

    switch (command) {
      case 'f':  // Forward
        direction = true;
        startMotor();
        Serial.println("Motor running forward");
        break;

      case 'b':  // Backward
        direction = false;
        startMotor();
        Serial.println("Motor running backward");
        break;

      case 's':  // Stop
        stopMotor();
        Serial.println("Motor stopped");
        break;

      case '+':  // Increase speed
        motorSpeed = min(motorSpeed + 10, 255);
        Serial.printf("Speed increased to %d\n", motorSpeed);
        startMotor();  // Update motor speed
        break;

      case '-':  // Decrease speed
        motorSpeed = max(motorSpeed - 10, 0);
        Serial.printf("Speed decreased to %d\n", motorSpeed);
        startMotor();  // Update motor speed
        break;

      default:
        Serial.println("Invalid command. Use 'f', 'b', 's', '+', or '-'.");
        break;
    }
  }
}

// Function to start the motor
void startMotor() {
  if (direction) {
    analogWrite(A1, motorSpeed);  // Set IN1 to PWM speed
    analogWrite(A2, 0);
  } else {
    analogWrite(A1, 0);  // Set IN1 to PWM speed
    analogWrite(A2, motorSpeed);
  }
}

// Function to stop the motor
void stopMotor() {
  analogWrite(A1, 0);
  analogWrite(A2, 0);
}
