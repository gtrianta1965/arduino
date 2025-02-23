from microdot import Microdot, Response, WebSocket
import json

app = Microdot()
Response.default_content_type = 'text/html'

# Store initial parameter values
parameters = {
    "switch1": False,
    "switch2": False,
    "slider1": 128,
    "slider2": 50,
    "num1": 5,
    "num2": 10
}

# Serve HTML file
@app.route('/')
def index(request):
    try:
        with open('menu1.html', 'r') as f:
            return Response(f.read())
    except:
        return "Error: index.html not found", 404

# WebSocket Handler
@app.route('/ws')
def websocket_handler(request, ws: WebSocket):
    print("WebSocket Connected")

    # Send initial values
    ws.send(json.dumps(parameters))

    while True:
        try:
            message = ws.receive()
            if message:
                data = json.loads(message)

                # Update parameters
                parameters.update(data)
                print("Updated Parameters:", parameters)

                # Send updated values back to all clients
                ws.send(json.dumps(parameters))

        except Exception as e:
            print("WebSocket Error:", e)
            break

    print("WebSocket Disconnected")
    return ''

# Start the server
app.run(host='0.0.0.0', port=80)
