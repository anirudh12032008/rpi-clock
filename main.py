import utime
from machine import Pin, SoftI2C, Pin, PWM
from pico_i2c_lcd import I2cLcd
from time import sleep
import time
from ds1307 import DS1307
print("hiiii")

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

i2c_rtc = SoftI2C(sda=Pin(2), scl=Pin(3))
rtc = DS1307(i2c_rtc)

JOYSTICK_X_PIN = 26  
JOYSTICK_Y_PIN = 27  
JOYSTICK_SW_PIN = 28  

x_axis = machine.ADC(Pin(JOYSTICK_X_PIN))
y_axis = machine.ADC(Pin(JOYSTICK_Y_PIN))
sw = Pin(JOYSTICK_SW_PIN, Pin.IN, Pin.PULL_UP) 

def read_joystick():
    x_val = x_axis.read_u16()  
    y_val = y_axis.read_u16()  
    sw_val = sw.value()  

    return x_val, y_val, sw_val

BUZZER_PIN = 15
buzzer = PWM(Pin(BUZZER_PIN))

BUTTON_PIN = 22
button = Pin(BUTTON_PIN, Pin.IN) 

def is_button_pressed():
    return button.value() == 0  

lcd.putstr("It's working :)")
sleep(2)


def buzz():
    buzzer.freq(1000)
    buzzer.duty_u16(32768)
    time.sleep(0.1)
    buzzer.duty_u16(0)

sleep(1)
buzz()
sleep(1)

try:
    while True:
        lcd.clear()
        current_time = rtc.datetime()
        formatted_time = f"{current_time[4]:02}:{current_time[5]:02}:{current_time[6]:02}"  # HH:MM:SS
        
        lcd.putstr(f"Time: {formatted_time}")
        x_val, y_val, sw_val = read_joystick()
        if is_button_pressed():
            print("Button Pressed!")
            buzz()  
        print(f"X: {x_val}, Y: {y_val}, Button: {sw_val}")
        sleep(1)

except KeyboardInterrupt:
    print("Keyboard interrupt")
    lcd.backlight_off()
    lcd.display_off()