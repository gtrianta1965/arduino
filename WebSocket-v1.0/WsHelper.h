#ifndef WS_HELPER_H
#define WS_HELPER_H
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>


class WsHelper {
public:
  WsHelper(const char index_html[])
    : server(80), ws("/ws"), _index_html(index_html) {
  }

  void begin() {

    ws.onEvent([this](AsyncWebSocket *server, AsyncWebSocketClient *client,
                      AwsEventType type, void *arg, uint8_t *data, size_t len) {
      eventHandler(server, client, type, arg, data, len);
    });

    server.addHandler(&ws);

    // Route for root / web page
    server.on("/", HTTP_GET, [this](AsyncWebServerRequest *request) {
      request->send_P(200, "text/html", _index_html,
                      [this](const String &var) -> String {
                        return this->processor(var);
                      });
    });

    // Start server
    server.begin();
  }
  void cleanUpClients() {
    //ws.cleanupClients();
  }

private:

  void handleWebSocketMessage(void *arg, uint8_t *data, size_t len) {

    AwsFrameInfo *info = (AwsFrameInfo *)arg;
    if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
      data[len] = 0;
      Serial.printf("Data=%s\n",data);
      if (strcmp((char *)data, "toggle") == 0) {
        //ledState = !ledState;
        //ws.textAll(String(ledState));
      }
    }
  }

  void eventHandler(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len) {

    switch (type) {
      case WS_EVT_CONNECT:
        Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
        break;
      case WS_EVT_DISCONNECT:
        Serial.printf("WebSocket client #%u disconnected\n", client->id());
        break;
      case WS_EVT_DATA:
        Serial.println("Data arrived");
        handleWebSocketMessage(arg, data, len);
        //digitalWrite(ledPin, ledState);
        break;
      case WS_EVT_PONG:
      case WS_EVT_ERROR:
        break;
    }
  }


  String processor(const String &var) {
    /*
    if (var == "STATE") {
      return ledState ? "ON" : "OFF";
    }
    if (var == "CHECK") {
      return ledState ? "checked" : "";
    }
    return String();
  */
  }


  AsyncWebServer server;
  AsyncWebSocket ws;
  const char *_index_html;
};

#endif