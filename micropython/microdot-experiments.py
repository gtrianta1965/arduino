from microdot import Microdot
import network
import time
import urequests
import asyncio

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


app = Microdot()

html = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
async def hello(request):
    return html, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

@app.get("/g30")
async def say(request):
    return "Hello G30",200

url = "https://www.flash.gr"  # Change to your URL

try:
    response = urequests.get(url)  # Send GET request
    print("Status Code:", response.status_code)  # Print status
    #print("Response:", response.text)  # Print content (optional)
    response.close()  # Close the connection
except Exception as e:
    print("Request failed:", e)
    
async def main():
    # start the server in a background task
    server = asyncio.create_task(app.start_server())

    # ... do other asynchronous work here ...

    # cleanup before ending the application
    await server

asyncio.run(main())
#app.run(debug=True)
print("Server started")
