import tm1637
from machine import Pin, Timer, PWM
from time import sleep
import time

tm_black = tm1637.TM1637(clk=Pin(0), dio=Pin(1)) #player1 button
tm_white = tm1637.TM1637(clk=Pin(2), dio=Pin(3)) #player2 button

button_set_time = Pin(5, Pin.IN, Pin.PULL_UP)  # top button (set time)
btn_pause_resume = Pin(4, Pin.IN, Pin.PULL_UP)  # bottom button (pause/resume)

btn_white = Pin(20, Pin.IN, Pin.PULL_UP)
btn_black = Pin(21, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(6))
buzzer.duty(0) #Set it to off

# Timer Variables
start_time = 5 * 60
initial_time = start_time  # Default start time in seconds
time_white = initial_time
time_black = initial_time
active_player = "white"
game_running = False  # Game starts in paused mode
time_increase_step = 5 * 60
maximum_time = 31 * 60

# Debounce and Timer
debounce_time = 300  # in ms
last_interrupt_time = 0  # Prevents button bouncing

def play_tone(frequency, duration):
    buzzer.freq(frequency)  # Set frequency (e.g., 1000Hz)
    buzzer.duty(500)  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty(0)  # Turn off sound
    
    
def update_display():
    """Updates both displays with the current time"""
    tm_white.show("{:02d}{:02d}".format(time_white // 60, time_white % 60),True)
    tm_black.show("{:02d}{:02d}".format(time_black // 60, time_black % 60),True)


def change_time(pin):
    """Interrupt function to increase the start time"""
    global initial_time, time_white, time_black, last_interrupt_time,active_player,game_running
    now = time.ticks_ms()
    
    if time.ticks_diff(now, last_interrupt_time) > debounce_time:
        initial_time += time_increase_step # 60  # Increase by 1 minute
        initial_time = initial_time if initial_time < maximum_time else start_time
        time_white = initial_time 
        time_black = initial_time
        update_display()
        last_interrupt_time = now
        game_running = False
        active_player = "white"

def switch_turn(pin):
    
    """Switch player turns"""
    global active_player, game_running
    if not game_running:
        return  # Ignore if game is paused
    
    # check that the button has been pressed from the active player (he finished his move)
    if pin == Pin(20) and active_player == "white":
       active_player = "black"
    if pin == Pin(21) and active_player == "black":
       active_player = "white"


def toggle_pause_resume(pin):
    """Toggles between pausing and resuming the game"""
    global game_running, last_interrupt_time
    now = time.ticks_ms()

    if time.ticks_diff(now, last_interrupt_time) > debounce_time:
        game_running = not game_running  # Toggle state
        last_interrupt_time = now


def countdown(timer):
    
    """Decreases time every second for the active player"""
    global time_white, time_black, active_player, game_running

    print(f"Active player is {active_player}, game is running={game_running}")
    if not game_running:
        return  # Stop countdown if paused

    if active_player == "white":
        if time_white > 0:
            time_white -= 1
        else:
            #buzzer.on()
            play_tone(1000,3)
            game_running = False  # Stop the game
    else:
        if time_black > 0:
            time_black -= 1
        else:
            #buzzer.on()
            play_tone(1000,3)
            game_running = False  # Stop the game

    update_display()


# Attach interrupts
button_set_time.irq(trigger=Pin.IRQ_FALLING, handler=change_time)
btn_white.irq(trigger=Pin.IRQ_FALLING, handler=switch_turn)
btn_black.irq(trigger=Pin.IRQ_FALLING, handler=switch_turn)
btn_pause_resume.irq(trigger=Pin.IRQ_FALLING, handler=toggle_pause_resume)

# Start countdown timer
game_timer = Timer(0)
game_timer.init(period=1000, mode=Timer.PERIODIC, callback=countdown)

update_display()