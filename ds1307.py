from machine import I2C
import utime

DS1307_I2C_ADDR = 0x68

class DS1307:
    def __init__(self, i2c):
        self.i2c = i2c

    def _bcd_to_dec(self, bcd):
        return (bcd >> 4) * 10 + (bcd & 0x0F)

    def _dec_to_bcd(self, dec):
        return ((dec // 10) << 4) + (dec % 10)

    def datetime(self, dt=None):
        if dt is None:
            data = self.i2c.readfrom_mem(DS1307_I2C_ADDR, 0x00, 7)
            seconds = self._bcd_to_dec(data[0] & 0x7F)
            minutes = self._bcd_to_dec(data[1])
            hours = self._bcd_to_dec(data[2])
            weekday = self._bcd_to_dec(data[3])
            day = self._bcd_to_dec(data[4])
            month = self._bcd_to_dec(data[5])
            year = self._bcd_to_dec(data[6]) + 2000
            return (year, month, day, weekday, hours, minutes, seconds, 0)
        else:
            self.i2c.writeto_mem(DS1307_I2C_ADDR, 0x00, bytearray([
                self._dec_to_bcd(dt[6]),
                self._dec_to_bcd(dt[5]),
                self._dec_to_bcd(dt[4]),
                self._dec_to_bcd(dt[3]),
                self._dec_to_bcd(dt[2]),
                self._dec_to_bcd(dt[1]),
                self._dec_to_bcd(dt[0] - 2000),
            ]))
            # Enable the clock if it was previously disabled
            seconds = self.i2c.readfrom_mem(DS1307_I2C_ADDR, 0x00, 1)[0] & 0x7F
            self.i2c.writeto_mem(DS1307_I2C_ADDR, 0x00, bytes([seconds]))

    def start(self):
        seconds = self.i2c.readfrom_mem(DS1307_I2C_ADDR, 0x00, 1)[0] & 0x7F
        self.i2c.writeto_mem(DS1307_I2C_ADDR, 0x00, bytes([seconds]))

    def stop(self):
        seconds = self.i2c.readfrom_mem(DS1307_I2C_ADDR, 0x00, 1)[0] | 0x80
        self.i2c.writeto_mem(DS1307_I2C_ADDR, 0x00, bytes([seconds]))

    def is_running(self):
        return not bool(self.i2c.readfrom_mem(DS1307_I2C_ADDR, 0x00, 1)[0] & 0x80)
