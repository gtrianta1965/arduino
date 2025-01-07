#include "WebSocketManager.h"
#include <LittleFS.h>
#include "MyLib.h"


WebSocketManager::WebSocketManager(AsyncWebServer& server, const char* endpoint, const char* htmlFilePath)

  : webSocket(new AsyncWebSocket(endpoint)), _htmlFilePath(htmlFilePath) {

  server.addHandler(webSocket);

  if (!LittleFS.begin()) {
    Serial.println("An Error has occurred while mounting SPIFFS");
  }

  server.on("/", HTTP_GET, [this](AsyncWebServerRequest* request) {
    if (LittleFS.exists(_htmlFilePath)) {
      LOG("File %s served from LittleFS\n", _htmlFilePath);
      request->send(LittleFS, _htmlFilePath, "text/html");
    } else {
      LOG("File not found from LittleFS (%s)\n", _htmlFilePath);
      request->send(404, "text/plain", "File not found");
    }
  });



  webSocket->onEvent([this](AsyncWebSocket* server, AsyncWebSocketClient* client,

                            AwsEventType type, void* arg, uint8_t* data, size_t len) {
    handleWebSocketEvent(server, client, type, arg, data, len);
  });
}



WebSocketManager::~WebSocketManager() {

  delete webSocket;
}



void WebSocketManager::onMessage(std::function<void(uint32_t clientId, const String& message)> callback) {

  messageHandler = callback;
}



void WebSocketManager::onConnect(std::function<void(uint32_t clientId)> callback) {

  connectHandler = callback;
}



void WebSocketManager::onDisconnect(std::function<void(uint32_t clientId)> callback) {

  disconnectHandler = callback;
}



void WebSocketManager::broadcast(const String& message) {

  webSocket->textAll(message);
}



void WebSocketManager::sendToClient(uint32_t clientId, const String& message) {

  AsyncWebSocketClient* client = webSocket->client(clientId);

  if (client && client->status() == WS_CONNECTED) {

    client->text(message);
  }
}



void WebSocketManager::cleanup() {

  webSocket->cleanupClients();
}



void WebSocketManager::handleWebSocketEvent(AsyncWebSocket* server, AsyncWebSocketClient* client,

                                            AwsEventType type, void* arg, uint8_t* data, size_t len) {

  switch (type) {

    case WS_EVT_CONNECT:

      LOG("Connect event from %s -> ", client->remoteIP().toString());

      if (connectHandler) connectHandler(client->id());

      break;

    case WS_EVT_DISCONNECT:

      LOG("Disconnect event from %s -> ", client->remoteIP().toString());

      if (disconnectHandler) disconnectHandler(client->id());

      break;

    case WS_EVT_DATA:
      {

        LOG("Data  event from %s -> ", client->remoteIP().toString());
        AwsFrameInfo* info = (AwsFrameInfo*)arg;

        if (info->opcode == WS_TEXT) {

          String message = String((char*)data).substring(0, len);

          if (messageHandler) messageHandler(client->id(), message);
        }

        break;
      }

    default:

      break;
  }
}