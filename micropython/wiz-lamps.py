import network
import time
from socket import *
import json

# Wi-Fi Credentials
SSID = "TP-Link_1196"
PASSWORD = "50874811"

# SSID = "Vodafone-E77640838"
# PASSWORD = "4JAbcK3GGxKN3sr6"

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

# create UDP socket
sock = socket(AF_INET, SOCK_DGRAM)
#sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.settimeout(14)

server_address = ("192.168.2.23", 38899)
message: str = r'{"method":"registration","params":{"phoneMac":"AAAAAAAAAAAA","register":false,"phoneIp":"1.2.3.4",' \
               r'"id":"1"}} '
discovered: list = []


def discover():
    print("Discovering")
    sock.sendto(message.encode(), server_address)
    while True:

        # get response
        try:
            data, server = sock.recvfrom(4096)
            if """"success":true""" in data.decode() and not discovered.__contains__(str(server[0])):
                discovered.append(str(server[0]))
        except Exception as err:
            print("done discovering",err)
            break
    return discovered
command = {
    "method": "setState",
    "params": {"state": False}  # Set to False to turn off
}
discover_msg = {
    "method": "getSystemConfig",
    "params": {}
}

sock.sendto(json.dumps(command).encode(), server_address)
response, _ = sock.recvfrom(1024)
print("Response:", response.decode())

#sock.sendto(json.dumps(discover_msg).encode(), server_address)
#response, _ = sock.recvfrom(1024)
#print("Response:", response.decode())

#a = discover()
#print("Result",a)
