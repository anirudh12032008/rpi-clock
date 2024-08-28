from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from ds1307 import DS1307
import utime
import time

i2c_lcd = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c_lcd, 0x27, 2, 16)

i2c_rtc = I2C(1, sda=Pin(2), scl=Pin(3))
rtc = DS1307(i2c_rtc)

def display_time():
    now = rtc.datetime()
    lcd.clear()
    lcd.putstr(f"{now[4]:02}:{now[5]:02}:{now[6]:02}") 
    utime.sleep(1)

while True:
    display_time()
    time.sleep(2)
    print("hi")