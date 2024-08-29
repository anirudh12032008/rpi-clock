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



BUZZER_PIN = 15
buzzer = PWM(Pin(BUZZER_PIN))


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
        sleep(1)

except KeyboardInterrupt:
    print("Keyboard interrupt")
    lcd.backlight_off()
    lcd.display_off()