from wifilib import wifilib as w
from microdot import Microdot, Response,send_file
from microdot.websocket import with_websocket
import json
import uasyncio as asyncio
from machine import Pin
import network
import urequests
import binascii
from config import ConfigManager

SSID = "TP-Link_1196"
PASSWORD = "50874811"
# Static IP details
STATIC_IP = '192.168.2.210'
GATEWAY = '192.168.2.1'
NETMASK = '255.255.255.0'

led = Pin(5,Pin.OUT)
config = ConfigManager()
hostname = config.get('hostname')


async def blink_led():
    global wlan
    while True:
        if not wlan.isconnected():
           led.value(not led.value())
           #print("Blinking")
           await asyncio.sleep(0.4)
        else:
           led.on()
           await asyncio.sleep(2)
#a = w(hostname = "ESP32SMV3")


wlan = network.WLAN(network.STA_IF)

app = Microdot()
Response.default_content_type = 'text/html'

# Store initial parameter values
parameters = {
    "switch1": False,
    "switch2": False,
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

async def connect_wifi():
    global wlan
    
    print("Inactivate Wifi")
    wlan.active(False)
    await asyncio.sleep(1)
    print("Activate Wifi")
    wlan.active(True)
    await asyncio.sleep(2)
    print("Disconnect")
    wlan.disconnect()
    await asyncio.sleep(2)
    
    
    
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        #wlan.ifconfig((STATIC_IP, NETMASK, GATEWAY, GATEWAY)) #assign a static IP
        network.hostname(hostname)
        print("MAC Address:",binascii.hexlify(wlan.config('mac'), ':').decode())
        wlan.config(dhcp_hostname=hostname,txpower=76)  # txpower is a magic value to enhance the signal especially for ESP32 C3 Super Mini
        await asyncio.sleep(2)
        wlan.connect(SSID, PASSWORD)
        
        for _ in range(40):  # Wait up to 20 seconds
            if wlan.isconnected():
                print("Connected! IP:", wlan.ifconfig())
                # Perform an outbound call to check internet
                url = "https://www.flash.gr"  # Change to your URL

                try:
                    print("Checking outbound internet connectivity to {url}")
                    response = urequests.get(url)  # Send GET request
                    print("Status Code:", response.status_code)  # Print status
                    #print("Response:", response.text)  # Print content (optional)
                    response.close()  # Close the connection
                except Exception as e:
                    print("Request failed:", e)
                return
            await asyncio.sleep(1)
        
        print("Wi-Fi connection failed.")
    else:
        print("Already connected!")
async def start_server():
    print("Starting Microdot server...")
    await app.start_server(port=80,debug=True)
    
async def main():
    task1 = asyncio.create_task(blink_led())
    task2 = asyncio.create_task(connect_wifi())
    task3 = asyncio.create_task(start_server())

    # Run all tasks indefinitely
    await asyncio.gather(task1, task2, task3)
    

# Start the server
asyncio.run(main())




