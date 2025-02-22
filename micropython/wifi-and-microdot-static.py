import network
import time
from microdot import Microdot

# Wi-Fi credentials
SSID = "TP-Link_1196"
PASSWORD = "50874811"

# Static IP details
STATIC_IP = '192.168.2.210'
GATEWAY = '192.168.2.1'
NETMASK = '255.255.255.0'

# Create a Microdot app
app = Microdot()

# Connect to Wi-Fi with Static IP
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Set static IP, Gateway, and Netmask using the correct method
    wlan.ifconfig((STATIC_IP, NETMASK, GATEWAY, GATEWAY))
    
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    
    while not wlan.isconnected():
        time.sleep(1)
    
    print("Connected to Wi-Fi")
    print("IP Address:", wlan.ifconfig()[0])

# Define route to handle HTTP requests
@app.route('/')
def index(request):
    return "Welcome to the ESP32-C3 web server!"

@app.route('/hello')
def hello(request):
    return "Hello from ESP32-C3!"

# Main execution
connect_wifi()  # Connect to Wi-Fi with static IP
app.run(host='0.0.0.0', port=80)  # Run the web server on port 80
