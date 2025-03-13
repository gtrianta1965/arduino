import network
import time
import asyncio
from config import ConfigManager
import binascii

class wifilib:
    NETWORKS = {
        "TP-Link_1196": "50874811",
        "Vodafone-E77640838" : "4JAbcK3GGxKN3sr6"
    }
    
    def __init__(self,hostname = "ESP32C3SM2", monitor_time = 30):
        print("Wifilib initialized")
        config = ConfigManager()
        self.hostname = config.get("hostname")
        self.monitor_time = monitor_time
        if self.hostname is not None:
            print(f"hostname={self.hostname} (from config)")
        else:
            print(f"No hostname found in config. Default {hostname}")
            self.hostname = hostname
        
        self.wlan = network.WLAN(network.STA_IF)
        print("MAC Address:",binascii.hexlify(self.wlan.config('mac'), ':').decode())
 
        self.best_ssid = None
        self.best_rssi = -100  # Very low signal strength to start
        
    def reconnect(self):
        print("try to reconnect")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)
        time.sleep(2)
 
        self.wlan.active(True)
        self.wlan.disconnect()
        time.sleep(2)
        self.connect()
    async def connect(self, scan = False):
        print("Connect called")
        
        self.wlan.active(False)
        await asyncio.sleep(2)
 
        self.wlan.active(True)
        await asyncio.sleep(2)
        self.wlan.disconnect()
        await asyncio.sleep(2)
        network.hostname(self.hostname)
        self.wlan.config(dhcp_hostname=self.hostname,txpower=76)  #txpower=76)  # txpower is a magic value to enhance the signal especially for ESP32 C3 Super Mini
        await asyncio.sleep(2)
        self.wlan.active(True)        
        
        
        if scan:
            self.list_wifi()
        if self.wlan.isconnected():
            print(f"We are connected. {self.wlan.ifconfig()} {self.wlan.config('essid')}, hostname={self.hostname}")
        else:
            if self.best_ssid:
                print(f"Connecting to {self.best_ssid} with signal strength {self.best_rssi}dBm")
                self.wlan.connect(self.best_ssid, self.NETWORKS[self.best_ssid])
                
                while not self.wlan.isconnected():
                    print(f".{self.wlan.status()}", end="")
                    await asyncio.sleep(1)

                print("\nConnected to:", self.best_ssid)
                print("IP Address:", self.wlan.ifconfig()[0],"Hostname",self.hostname)
            else:
                print("No known networks found.")
   
    def status(self):
        if self.wlan.isconnected():
           print(f"Connected ({self.best_ssid}), status={self.wlan.status()}")
        else:
           print(f"Not connected, status={self.wlan.status()}")
    def list_wifi(self, show_details = True):
        available_networks = self.wlan.scan()
        self.best_ssid = None
        self.best_rssi = -100  # Very low signal strength to start
        
        for net in available_networks:
            ssid = net[0].decode('utf-8')
            rssi = net[3]
            if ssid in self.NETWORKS and rssi > self.best_rssi:
               self.best_ssid = ssid
               self.best_rssi = rssi
            print(f"{ssid:20s}{rssi:>3.0f}db")
        print(f"\nFound {len(available_networks)} wifi networks")
        print(f"Best wifi is {self.best_ssid} with signal strength {self.best_rssi}dBm")
    def isconnected(self):
        return self.wlan.isconnected()
    
    async def monitor():
        while True:
            if (not wlan.isconnected()):
                print("Monitor WIFI: Lost connection, try to reconnect")
                await self.connect_wifi()
            else:
                print("Monitor WIFI: We are connected",)
        await asyncio.sleep(self.monitor_time)
        

if __name__ == "__main__":
    a = wifilib()
    #a.list_wifi()
    a.connect(scan = True)

    while True:
        a.status()
        time.sleep(10)
        if not a.isconnected():
            a = wifilib()
            a.connect(scan = True)


    