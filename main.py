import utime
from machine import Pin, SoftI2C, Pin
from pico_i2c_lcd import I2cLcd
from time import sleep
import time

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

lcd.putstr("It's working :)")
sleep(4)



try:
    while True:
	
        lcd.clear()
        lcd.putstr("Hello World!")
        sleep(2)
        lcd.clear()
        lcd.move_to(0, 1)
        lcd.putstr("Hello World!")
        sleep(2)

except KeyboardInterrupt:
    # Turn off the display
    print("Keyboard interrupt")
    lcd.backlight_off()
    lcd.display_off()