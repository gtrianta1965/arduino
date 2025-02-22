import uasyncio as asyncio
from microdot import Microdot, Response
from microdot.websocket import with_websocket
import machine
import network
import time

# LED on GPIO 2 (Change if needed)
led = machine.Pin(8, machine.Pin.OUT)

# Default blink delay (in seconds)
blink_delay = 0.5

# Create Microdot app
app = Microdot()
Response.default_content_type = "text/html"

# HTML Page (served at root "/")
html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 LED Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
        input { width: 100px; font-size: 20px; }
    </style>
    <script>
        let socket = new WebSocket("ws://" + location.host + "/ws");
        function sendDelay() {
            let delay = document.getElementById("delay").value;
            socket.send(delay);
        }
    </script>
</head>
<body>
    <h1>ESP32 LED Blinker</h1>
    <p>Set LED Blink Delay (seconds):</p>
    <input id="delay" type="number" value="0.5" step="0.1">
    <button onclick="sendDelay()">Set Delay</button>
</body>
</html>
"""

ssid = 'TP-Link_1196'
password = '50874811'

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(2)

#wlan.ifconfig(("192.168.2.214","255.255.255.0","192.168.2.1","192.168.2.1"))
wlan.active(True)
time.sleep(2)
wlan.connect(ssid, password)

time.sleep(2)
while wlan.isconnected() == False:
  print(".")
  time.sleep(1)

print('Connection successful')
print(wlan.ifconfig())

@app.route("/")
async def index(request):
    return html

# WebSocket to receive blink delay updates
@app.route("/ws")
@with_websocket
async def websocket_handler(request, ws):
    global blink_delay
    print(f"/ws called with request {request} and ws {ws}")
    while True:
        data = await ws.receive()
        try:
            blink_delay = float(data)
            print(f"New blink delay: {blink_delay}s")
        except ValueError:
            print("Invalid delay received")

# Asynchronous LED Blinking Task
async def blink_led():
    global blink_delay
    while True:
        led.value(1)
        await asyncio.sleep(blink_delay)
        led.value(0)
        await asyncio.sleep(blink_delay)

# Start Server and Tasks
async def main():
    asyncio.create_task(blink_led())  # Run LED blinking in background
    await app.start_server(port=80)   # Start Microdot server

# Run Async Main Function
asyncio.run(main())
