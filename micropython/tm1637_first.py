import tm1637
from machine import Pin
from time import sleep

tm1= tm1637.TM1637(clk=Pin(0), dio=Pin(1)) #player1 button
tm2= tm1637.TM1637(clk=Pin(2), dio=Pin(3)) #player2 button

btn_set_time = Pin(5, Pin.IN, Pin.PULL_UP)  # top button (set time)
btn_pause_resume = Pin(4, Pin.IN, Pin.PULL_UP)  # bottom button (pause/resume)

btn_white = Pin(20, Pin.IN, Pin.PULL_UP)
btn_black = Pin(21, Pin.IN, Pin.PULL_UP)

# Default countdown time (5 minutes = 300 seconds)
initial_time = 300
p1_time = initial_time
p2_time = initial_time
current_player = 1  #  1 = player1 , 2=player3 


def display_time(tm, seconds):
    """Display time in MM:SS format on TM1637."""
    minutes = seconds // 60
    secs = seconds % 60
    tm.show("{:02d}{:02d}".format(minutes, secs),True)

# Initial Display
display_time(tm1, p1_time)
display_time(tm2, p2_time)

def switch_turn():
    global current_player
    if current_player == 1:
        current_player = 2
    else:
        current_player = 1

while True:
    if btn_set_time.value() == 0:
        print("Set time pressed")
        sleep(0.2)
    if btn_pause_resume.value() == 0:
        print("Pause/Resume pressed")
        sleep(0.2)
    
    if btn_black.value() == 0:  # Player 1 finishes move
        print("Black finised")
        switch_turn()
        sleep(0.2)
    if btn_white.value() == 0:  # Player 2 finishes move
        print("White finised")
        switch_turn()
        sleep(0.2)
        

    if current_player == 1 and p1_time > 0:
        p1_time -= 1
        display_time(tm1, p1_time)
    elif current_player == 2 and p2_time > 0:
        p2_time -= 1
        display_time(tm2, p2_time)
    sleep(1)  # Countdown step

        
        

# tm1.show("3033",True)
# time.sleep(2)
# tm1.show("    ",False)
# 
# tm2.show("3033",True)
# time.sleep(2)
# tm2.show("    ",False)
# 
# while True:
#     print(btn_white.value())
#     time.sleep(0.2)