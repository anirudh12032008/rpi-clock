import utime
from machine import Pin, SoftI2C, PWM, ADC
from pico_i2c_lcd import I2cLcd
from time import sleep
from ds1307 import DS1307

I2C_ADDR = 0x27
ROWS, COLS = 2, 16

i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, ROWS, COLS)

rtc_i2c = SoftI2C(sda=Pin(2), scl=Pin(3))
rtc = DS1307(rtc_i2c)

X_PIN, Y_PIN, SW_PIN = 26, 27, 28

x_adc = ADC(Pin(X_PIN))
y_adc = ADC(Pin(Y_PIN))
sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

MODE_CLOCK, MODE_TIMER, MODE_STOPWATCH, MODE_ALARM = 0, 1, 2, 3

mode = MODE_CLOCK
timer_start, stopwatch_start, alarm = None, None, None

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
    if alarm:
        h, m = rtc.datetime()[4:6]
        if (h, m) == alarm:
            update_lcd("Alarm ringing!")
            buzz()

B_PIN = 15
buzzer = PWM(Pin(B_PIN))

BTN_PIN = 22
btn = Pin(BTN_PIN, Pin.IN)

def btn_pressed():
    return btn.value() == 0  

def debounce_btn(ms=200):
    last_state = btn.value()
    utime.sleep_ms(ms)
    return btn.value() == 0 and last_state == 0

update_lcd("It's working :)")
sleep(2)

def buzz():
    buzzer.freq(1000)
    buzzer.duty_u16(32768)
    sleep(0.1)
    buzzer.duty_u16(0)

sleep(1)
buzz()
sleep(1)

try:
    update_lcd("Welcome!")
    while True:
        x, y, sw_val = read_joystick()
        if btn_pressed():
            if mode == MODE_CLOCK:
                update_lcd("Switching mode...")
                mode = (mode + 1) % 4
                sleep(1)
            elif mode == MODE_TIMER:
                timer()
                sleep(1)
            elif mode == MODE_STOPWATCH:
                stopwatch()
                sleep(1)
            elif mode == MODE_ALARM:
                now = rtc.datetime()
                set_alarm(now[4], now[5])
                sleep(1)

        if x < 1000:
            mode = (mode + 1) % 4  
            sleep(0.2)
        elif x > 60000:
            mode = (mode - 1) % 4  
            sleep(0.2)

        if mode == MODE_CLOCK:
            t = rtc.datetime()
            update_lcd(f"Time: {t[4]:02}:{t[5]:02}:{t[6]:02}")
        elif mode == MODE_TIMER:
            timer()
        elif mode == MODE_STOPWATCH:
            stopwatch()
        elif mode == MODE_ALARM:
            check_alarm()
        
        sleep(1)

except KeyboardInterrupt:
    lcd.backlight_off()
    lcd.display_off()
