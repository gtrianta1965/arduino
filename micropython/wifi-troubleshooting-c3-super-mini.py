import network
import time

# 200: BEACON_TIMEOUT
# 201: NO_AP_FOUND
# 202: WRONG_PASSWORD
# 203: ASSOC_FAIL
# 204: HANDSHAKE_TIMEOUT
# 1000: IDLE
# 1001: CONNECTING
# 1010: GOT_IP

SSID = "TP-Link_1196"
PASSWORD = "50874811"

wlan = network.WLAN(network.STA_IF)




print("Inactivate")
wlan.active(False)
time.sleep(10)

print("Status=",wlan.status())

print("Activate")
wlan.active(True)
wlan.ifconfig(("192.168.2.212", "255.255.255.0", "192.168.2.1", "192.168.2.1"))

time.sleep(1)
wlan.disconnect()
time.sleep(3)

print(wlan.config('mac') )
new_mac = b'\x02\x11\x22\x33\x42\x55'  # Change this to your custom MAC
wlan.config(dhcp_hostname="ESP32C3SM")

# Set the new MAC address
wlan.config(mac=new_mac)

time.sleep(2)
print("Scanning")
wlan.scan()
print("Finished scanning")


wlan.connect(SSID, PASSWORD)

timeout = 10  # Max wait time (seconds)
start_time = time.time()

while True:
    status = wlan.status()
    print("Status:", status)
    
    if status == 1010:  # Connected
        print("Connected! IP:", wlan.ifconfig()[0])
        break
    elif status in [201, 202, 203]:  # Errors
        print("Connection failed! Error code:", status)
        #break
    else:
        print("Status=",status)
    time.sleep(5)

if wlan.status() != 1010:
    print("Failed to connect. Check SSID, password, and signal strength.")
