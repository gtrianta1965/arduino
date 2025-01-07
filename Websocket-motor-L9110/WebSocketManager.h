#ifndef WEBSOCKETMANAGER_H

#define WEBSOCKETMANAGER_H



#include <ESPAsyncWebServer.h>

#include <functional>



class WebSocketManager {

public:

    WebSocketManager(AsyncWebServer& server, const char* endpoint, const char* htmlFilePath);

    ~WebSocketManager();



    void onMessage(std::function<void(uint32_t clientId, const String& message)> callback);

    void onConnect(std::function<void(uint32_t clientId)> callback);

    void onDisconnect(std::function<void(uint32_t clientId)> callback);



    void broadcast(const String& message);

    void sendToClient(uint32_t clientId, const String& message);

    void cleanup();



private:

    AsyncWebSocket* webSocket;
    const char* _htmlFilePath;

    std::function<void(uint32_t clientId, const String& message)> messageHandler;

    std::function<void(uint32_t clientId)> connectHandler;

    std::function<void(uint32_t clientId)> disconnectHandler;



    void handleWebSocketEvent(AsyncWebSocket* server, AsyncWebSocketClient* client, 

                              AwsEventType type, void* arg, uint8_t* data, size_t len);

};



#endif // WEBSOCKETMANAGER_H