from wifilib import wifilib as w
from microdot import Microdot, Response,send_file
from microdot.websocket import with_websocket
import json
import uasyncio as asyncio
from machine import Pin
#import network
import urequests
from  wifilib import wifilib

led = Pin(5,Pin.OUT)


async def blink_led():
    global wlan
    while True:
        if not wlan.isconnected():
           led.value(not led.value())
           #print("Blinking")
           await asyncio.sleep(0.4)
        else:
           if (parameters['switch1'] == "true"):
              led.on()
           else:
              led.off()
           await asyncio.sleep(0.2)

wlan = wifilib()
app = Microdot()
Response.default_content_type = 'text/html'

# Store initial parameter values
parameters = {
    "switch1": "true",
    "switch2": "false",
    "slider1": 128,
    "slider2": 50,
    "num1": 5,
    "num2": 10,
    "text1" : "Default",
    "text2" : "N/A"
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
    print("WebSocket Connected",ws)

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

async def connect_wifi():
    global wlan
    await wlan.connect(scan = True)
    
async def start_server():
    print("Starting Microdot server...")
    await app.start_server(port=80,debug=True)
    
async def monitor_wifi():
    while True:
        if (not wlan.isconnected()):
            print("Monitor WIFI: Lost connection, try to reconnect")
            await connect_wifi()
        else:
            print("Monitor WIFI: We are connected",)
        await asyncio.sleep(20)
    
async def main():
    task1 = asyncio.create_task(blink_led())
    task2 = asyncio.create_task(connect_wifi())
    await task2
    
    
    task3 = asyncio.create_task(start_server())
    task4 = asyncio.create_task(monitor_wifi())
    

    # Run all tasks indefinitely
    await asyncio.gather(task1, task3,task4)
    
    

# Start the server
asyncio.run(main())




