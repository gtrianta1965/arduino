import network
import time




# Define your SSIDs and passwords
NETWORKS = {
    "TP-Link_1196": "50874811",
    "Vodafone-E77640838" : "4JAbcK3GGxKN3sr6"
}

def scan_and_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.ifconfig(("192.168.2.213","255.255.255.0","192.168.2.1","192.168.2.1"))
    wlan.active(True)
    
    if wlan.isconnected():
        print(f"We are connected. {wlan.ifconfig()} {wlan.config('essid')}")
        
        return
    else:
        print("Lost connections.Retry")
        wlan.active(False)
        time.sleep(2)
        wlan.active(True)
        wlan = network.WLAN(network.STA_IF)

    
    print("Scanning for networks...")
    available_networks = wlan.scan()  # List of tuples (ssid, bssid, channel, RSSI, security, hidden)
    print(f"Found {len(available_networks)} networks")
    
    best_ssid = None
    best_rssi = -100  # Very low signal strength to start
    
    for net in available_networks:
        ssid = net[0].decode('utf-8')
        rssi = net[3]
        if ssid in NETWORKS and rssi > best_rssi:
            best_ssid = ssid
            best_rssi = rssi
    
    if best_ssid:
        print(f"Connecting to {best_ssid} with signal strength {best_rssi}dBm")
        wlan.connect(best_ssid, NETWORKS[best_ssid])
        
        for _ in range(20):  # Wait up to 10 seconds for connection
            if wlan.isconnected():
                print("Connected!")
                print("IP Address:", wlan.ifconfig()[0])
                return
            time.sleep(1)
        
        print("Failed to connect.", wlan.status())
    else:
        print("No known networks found.")

if __name__ == "__main__":
    scan_and_connect()
    while True:
        time.sleep(10)  # Periodically rescan every 30 seconds       
        scan_and_connect()