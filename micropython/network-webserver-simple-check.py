import network
import socket
import time

# Wi-Fi Credentials
SSID = 'TP-Link_1196'
PASSWORD = '50874811'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(2)

wlan.active(True)
wlan.disconnect()
time.sleep(2)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass  # Wait for connection

print("Connected! IP Address:", wlan.ifconfig()[0])

print("Connected! ESP32 IP:", wlan.ifconfig()[0])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))  
print("Connected to the internet!")

# HTML Content
html = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Web Server</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        h1 { color: blue; }
    </style>
</head>
<body>
    <h1>Hello from ESP32! Wow what a wifi</h1>
    <p>ESP32 is running a simple web server.</p>
</body>
</html>
"""

# Start Web Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 80))  # Bind to port 80
sock.listen(5)  # Allow up to 5 clients

print("Web server started...")

while True:
    conn, addr = sock.accept()  # Accept a connection
    print(f"New client connected: {addr}")
    request = conn.recv(1024)  # Receive request
    print("Request:", request.decode("utf-8"))

    conn.send(html)  # Send HTML response
    conn.close()  # Close connection

