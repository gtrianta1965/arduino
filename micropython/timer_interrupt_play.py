from machine import Timer
import time

time_to_fire = 10

timer1 = Timer(0)
timer2 = Timer(1)

print("Let's start")


def t1(timer):
    global time_to_fire
    print(f"Timer {timer} fired, counter = {time_to_fire}")
    print(time.localtime())
    if timer.value() == 0:
        time_to_fire = (time_to_fire - 1) if time_to_fire > 0 else 0
        if time_to_fire == 0:
            timer.deinit()
            print(f"timer {timer.value()} finished") 
        
    
def t2(timer):
    print("Timer 2 fired")
    
timer1.init(period=1000,mode=Timer.PERIODIC,callback=t1)
timer2.init(period=2000,mode=Timer.ONE_SHOT,callback=t1)

