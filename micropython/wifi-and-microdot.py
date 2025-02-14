import network
import time
from microdot import Microdot
from machine import Pin

# Wi-Fi Credentials
# SSID = "TP-Link_1196"
# PASSWORD = "50874811"

SSID = "Vodafone-E77640838"
PASSWORD = "4JAbcK3GGxKN3sr6"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Connecting to Wi-Fi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    
    print("\nConnected! IP:", wlan.ifconfig()[0])
    print("Connected",wlan.ifconfig())
    
    return wlan.ifconfig()[0]  # Return the assigned IP

# Connect and get IP
ip_address = connect_wifi()



app = Microdot()

# LED configuration (modify GPIO as needed)
LED_PIN = 2
led = Pin(LED_PIN, Pin.OUT)

# Web page
@app.route('/')
def index(request):
    html = f"""
    <html>
    <head><title>ESP32 Web Server</title></head>
    <body>
        <h1>ESP32 Microdot Server</h1>
        <p>Microdot is running on IP: {ip_address}</p>
        <a href="/led/on"><button>Turn LED On</button></a>
        <a href="/led/off"><button>Turn LED Off</button></a>
    </body>
    </html>
    """
    return html, 200, {'Content-Type': 'text/html'}

# LED Control Routes
@app.route('/led/<state>')
def led_control(request, state):
    if state == "on":
        #led.on()
        return "LED is ON", 200
    elif state == "off":
        #led.off()
        return "LED is OFF", 200
    return "Invalid request", 400

# Run server
print("Starting server")
app.run(host=ip_address, port=80)