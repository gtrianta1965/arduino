#include <ESPAsyncWebServer.h>

#include <WiFi.h>
#include <ArduinoJson.h>
#include "WebSocketManager.h"
#include "MyLib.h"



// Wi-Fi credentials
const char* ssid = "Vodafone-E77640838";
const char* password = "4JAbcK3GGxKN3sr6";

int speed = 50;
int steering = 0;
int isStopper = 0;

AsyncWebServer server(80);

WebSocketManager* wsManager;

void setup() {

    Serial.begin(115200);
    // Connect to Wi-Fi

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to Wi-Fi...");
    }

    Serial.print("Connected to Wi-Fi with IP");Serial.println(WiFi.localIP());
    // Initialize WebSocket Manager

    wsManager = new WebSocketManager(server, "/ws","/ws2.html");
    // Set WebSocket event handlers. Register the callbacks with Lamda anonymous function

    wsManager->onConnect([](uint32_t clientId) {
        Serial.printf("Client %u connected with IP %s\n", clientId);

    });

    wsManager->onDisconnect([](uint32_t clientId) {
        Serial.printf("Client %u disconnected\n", clientId);
    });



    wsManager->onMessage([](uint32_t clientId, const String& message) {

        Serial.printf("Received from client %u: %s\n", clientId, message.c_str());

        wsManager->sendToClient(clientId, "Echo: " + message);

    });

    // Start the server
    server.begin();

}



void loop() {

    // Clean up disconnected clients
    wsManager->cleanup();
}