from wifilib import wifilib as w
from microdot import Microdot, Response,send_file
from microdot.websocket import with_websocket
import json
import uasyncio as asyncio


a = w()
a.connect(scan = True)



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
    print("Route / , sending file")
    return send_file('menu1.html', content_type='text/html')

# WebSocket Handler
@app.route('/ws')
@with_websocket
async def websocket_handler(request, ws: WebSocket):
    print("WebSocket Connected")

    # Send initial values
    await ws.send(json.dumps(parameters))

    while True:
        try:
            message = await ws.receive()
            if message:
                print("Got message",message)
                data = json.loads(message)

                # Update parameters
                parameters.update(data)
                print("Updated Parameters:", parameters)

                # Send updated values back to all clients
                await ws.send(json.dumps(parameters))

        except Exception as e:
            print("WebSocket Error:", e)
            break

    print("WebSocket Disconnected")
    return ''

# Start the server
app.run(host='0.0.0.0', port=80)



