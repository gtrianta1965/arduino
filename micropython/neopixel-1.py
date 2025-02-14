import machine, neopixel
import time

n = 8
p = 5

np = neopixel.NeoPixel(machine.Pin(p), n)

def clear():
    for i in range(n):
        np[i] = (0,0,0)
    np.write()
    
while True:
    for k in range(20):
        for j in range(n):
            np[j] = (10+j*12, j*3,0)
        np.write()
        time.sleep(2)
        clear()
        time.sleep(2-k/10)
    
np[0] = (0, 10, 0)
#np[3] = (125, 204, 223)
#np[7] = (120, 153, 23)



np.write()