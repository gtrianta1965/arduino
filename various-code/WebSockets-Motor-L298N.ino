#include <WiFi.h>
#include <WebSocketsServer.h>

// WiFi credentials
const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";

// Motor pins
const int ENA = 32; // PWM pin for Motor A
const int IN1 = 25; // Direction pin for Motor A
const int IN2 = 26; // Direction pin for Motor A
const int ENB = 33; // PWM pin for Motor B
const int IN3 = 27; // Direction pin for Motor B
const int IN4 = 14; // Direction pin for Motor B

WebSocketsServer webSocket(81);

// Motor state variables
bool isRunning = false;
bool isForward = true;
int speed = 0;
int steering = 50; // 50 represents centered steering

void setup() {
  Serial.begin(115200);
  
  // Set motor pins as output
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  // Start WebSocket server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  webSocket.loop();
  controlMotors();
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_TEXT) {
    String message = (char*)payload;
    if (message.startsWith("start")) {
      isRunning = true;
    } else if (message.startsWith("stop")) {
      isRunning = false;
    } else if (message.startsWith("direction")) {
      isForward = (message.endsWith("forward"));
    } else if (message.startsWith("speed")) {
      speed = message.substring(6).toInt();
    } else if (message.startsWith("steering")) {
      steering = message.substring(9).toInt();
    }
  }
}

void controlMotors() {
  if (!isRunning) {
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);
    return;
  }

  // Set direction
  if (isForward) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  } else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }

  // Calculate speeds for steering
  int leftSpeed = speed;
  int rightSpeed = speed;

  if (steering < 50) { // Turn left
    rightSpeed = map(steering, 0, 50, 0, speed);
  } else if (steering > 50) { // Turn right
    leftSpeed = map(steering, 50, 100, speed, 0);
  }

  // Apply speeds
  analogWrite(ENA, leftSpeed);
  analogWrite(ENB, rightSpeed);
}
