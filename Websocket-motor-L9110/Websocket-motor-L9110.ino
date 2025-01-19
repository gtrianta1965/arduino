#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include "MyLib.h"
#include "WebSocketManager.h"

#define A1 25  // Motor A INA
#define A2 26  // Motor A INB

#define B1 32  // Motor B INA
#define B2 33  // Motor B INB

// WiFi credentials
const char* ssid = "Vodafone-E77640838";
const char* password = "4JAbcK3GGxKN3sr6";

// Motor pins

//Server and websocket variable
AsyncWebServer server(80);
WebSocketManager* wsManager;

// Motor state variables
bool isRunning = false;
bool isForward = true;
int speed = 0;
int steering = 50;  // 50 represents centered steering
bool speedOrSteeringChanged = false;
int leftSpeed = speed;
int rightSpeed = speed;

void setup() {
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  analogWrite(A1, 0);
  analogWrite(A2, 0);
  pinMode(B1, OUTPUT);
  pinMode(B2, OUTPUT);
  analogWrite(B1, 0);
  analogWrite(B2, 0);
  Serial.begin(115200);

  delay(1000);
  // Set motor pins as output


  LOG("Program start\n");

  // Connect to WiFi

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to Wi-Fi...");
  }
  Serial.print("Connected to Wi-Fi with IP:");
  Serial.println(WiFi.localIP());

  // Setup and Start WebSocket server
  wsManager = new WebSocketManager(server, "/ws", "/joystick1.html");
  // Set WebSocket event handlers. Register the callbacks with Lamda anonymous function

  wsManager->onConnect([](uint32_t clientId) {
    Serial.printf("Client %u connected with IP %s\n", clientId);
  });
  wsManager->onDisconnect([](uint32_t clientId) {
    Serial.printf("Client %u disconnected\n", clientId);
  });
  wsManager->onMessage([](uint32_t clientId, const String& message) {
    //LOG("Received from client %u: %s\n", clientId, message.c_str());
    //wsManager->sendToClient(clientId, "Echo: " + message);
    webSocketEvent(clientId,message);
  });
  // Start the server
  server.begin();
  controlMotors();
}

void loop() {
  wsManager->cleanup();
  //controlMotors();
}


void webSocketEvent(uint32_t clientId, const String& payload) {
    
    String message = payload;
    LOG("Received message:%s\n", message);
    if (message.startsWith("start")) {
      isRunning = true;
    } else if (message.startsWith("stop")) {
      isRunning = false;
    } else if (message.startsWith("direction")) {
      isForward = (message.endsWith("forward"));
    } else if (message.startsWith("speed")) {
      speedOrSteeringChanged = true;
      speed = message.substring(6).toInt();
      controlMotors();
    } else if (message.startsWith("steering")) {
      speedOrSteeringChanged = true;
      steering = message.substring(9).toInt();
      controlMotors();
    } 
    //LOG("isRunning=%d, isForoward=%d, speed=%d, steering=%d\n",isRunning,isForward,speed,steering); 
}


void controlMotors() {
  int _speed;
  int _steering;

  //normalize speed and steering
  isRunning = false;
  if (speed < 0) { isForward = false; isRunning = true;}
  if (speed > 0) { isForward = true; isRunning = true;}
  _speed = map(abs(speed),0,100,50,255);
  _steering = map(steering,-100,100,0,100); // normalize steering between 0 and 100

  if (!isRunning) {
    analogWrite(A1, 0);
    analogWrite(A2, 0);
    analogWrite(B1, 0);
    analogWrite(B2, 0);

    return;
  }

  // Calculate speeds for steering
  leftSpeed = _speed;
  rightSpeed = _speed;

  //adopt left and right speed according to steering
  if (_steering > 50) {
    // reduce speed of left weel
    rightSpeed = _speed - _speed * (_steering - 50 )/50;
    leftSpeed = _speed;
  } 
  if (_steering < 50) {
    // reduce speed of left weel
    leftSpeed = _speed - _speed * (50 - _steering )/50;
    rightSpeed = _speed;
  } 
  
  // Set direction
  if (isForward) {
    analogWrite(A2, 0);
    analogWrite(A1, leftSpeed);
    analogWrite(B2, 0);
    analogWrite(B1, rightSpeed);

  } else {
    analogWrite(A1, 0);
    analogWrite(A2, leftSpeed);
    analogWrite(B1, 0);
    analogWrite(B2, rightSpeed);

  }
  if (speedOrSteeringChanged) {
      //LOG("isRunning=%d, isForoward=%d, speed=%d, steering=%d,leftSpeed=%d,rightSpeed=%d\n",isRunning,isForward,_speed,_steering,leftSpeed,rightSpeed);  
      speedOrSteeringChanged = false;
  }
  // Apply speeds
  //analogWrite(ENB, rightSpeed);
}
