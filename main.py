import utime
from machine import Pin, SoftI2C, PWM, ADC
from pico_i2c_lcd import I2cLcd
from ds1307 import DS1307
from time import sleep


I2C_ADDR = 0x27
ROWS, COLS = 2, 16
X_PIN, Y_PIN, SW_PIN = 26, 27, 28
B_PIN = 15
BUTTON_PIN = 22  

MODE_CLOCK, MODE_TIMER, MODE_STOPWATCH, MODE_ALARM = 0, 1, 2, 3
mode = MODE_CLOCK
confirmed_mode = None
timer_start, stopwatch_start, alarm = None, None, None


i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, ROWS, COLS)
rtc_i2c = SoftI2C(sda=Pin(2), scl=Pin(3))
rtc = DS1307(rtc_i2c)
x_adc = ADC(Pin(X_PIN))
y_adc = ADC(Pin(Y_PIN))
sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(B_PIN))
btn = Pin(BUTTON_PIN, Pin.IN)

def update_lcd(txt):
    lcd.clear()
    lcd.putstr(txt)

def read_joystick():
    return x_adc.read_u16(), y_adc.read_u16(), sw.value()

def set_alarm(h, m):
    global alarm
    alarm = (h, m)
    update_lcd(f"Alarm Set: {h:02}:{m:02}")

def check_alarm():
    if alarm and rtc.datetime()[4:6] == alarm:
        update_lcd("Alarm ringing!")
        buzz()

def timer():
    global timer_start
    if timer_start is None:
        timer_start = utime.time()
        update_lcd("Timer started")
    else:
        elapsed = utime.time() - timer_start
        update_lcd(f"Timer: {elapsed // 60:02}:{elapsed % 60:02}")

def stopwatch():
    global stopwatch_start
    if stopwatch_start is None:
        stopwatch_start = utime.time()
        update_lcd("Stopwatch started")
    else:
        elapsed = utime.time() - stopwatch_start
        update_lcd(f"Stopwatch: {elapsed // 60:02}:{elapsed % 60:02}")

def buzz():
    buzzer.freq(1000)
    buzzer.duty_u16(32768)
    sleep(0.1)
    buzzer.duty_u16(0)

def btn_pressed():
    return btn.value() == 0  

MODE_NAMES = ["Clock", "Timer", "Stopwatch", "Alarm"]

try:
    lcd.display_on()
    update_lcd("Press button to start")
    
    while not btn_pressed():
        pass
    
    update_lcd("Welcome!")
    sleep(2)

    while True:
        x, y, sw_val = read_joystick()

        if confirmed_mode is None:  
            if x < 1000:  
                mode = (mode + 1) % 4
                update_lcd(f"Select Mode: {MODE_NAMES[mode]}")
                sleep(0.2)
            elif x > 60000: 
                mode = (mode - 1) % 4
                update_lcd(f"Select Mode: {MODE_NAMES[mode]}")
                sleep(0.2)

            if sw_val == 0:
                confirmed_mode = mode
                update_lcd(f"Mode {MODE_NAMES[confirmed_mode]} Confirmed")
                sleep(1)

        else: 
            if confirmed_mode == MODE_CLOCK:
                t = rtc.datetime()
                update_lcd(f"Time: {t[4]:02}:{t[5]:02}:{t[6]:02}")
            elif confirmed_mode == MODE_TIMER:
                timer()
            elif confirmed_mode == MODE_STOPWATCH:
                stopwatch()
            elif confirmed_mode == MODE_ALARM:
                check_alarm()

            if sw_val == 0:  
                confirmed_mode = None
                update_lcd("Returning to mode select...")
                sleep(1)

        sleep(1)

except KeyboardInterrupt:
    lcd.backlight_off()
    lcd.display_off()
