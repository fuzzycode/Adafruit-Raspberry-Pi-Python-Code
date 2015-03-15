#!/usr/bin/python

# Python library for Adafruit (L3GD20U).
# This is pretty much a direct port of the current Arduino library

# Copyright 2013 Adafruit Industries

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from Adafruit_I2C import Adafruit_I2C


class Adafruit_L3GD20_Unified(Adafruit_I2C):

    #=========================================================================
    # I2C ADDRESS/BITS AND SETTINGS
    #-------------------------------------------------------------------------
    L3GD20_ADDRESS           = 0x6B        # 1101011
    L3GD20_POLL_TIMEOUT      = 100         # Maximum number of read attempts
    L3GD20_ID                = 0xD4
    L3GD20H_ID               = 0xD7
    GYRO_SENSITIVITY_250DPS  = 0.00875     # Roughly 22/256 for fixed point match
    GYRO_SENSITIVITY_500DPS  = 0.0175      # Roughly 45/256
    GYRO_SENSITIVITY_2000DPS = 0.070       # Roughly 18/256


    #=========================================================================
    # REGISTERS
    #-------------------------------------------------------------------------

                                               # DEFAULT   TYPE
    GYRO_REGISTER_WHO_AM_I            = 0x0F   # 11010100   r
    GYRO_REGISTER_CTRL_REG1           = 0x20   # 00000111   rw
    GYRO_REGISTER_CTRL_REG2           = 0x21   # 00000000   rw
    GYRO_REGISTER_CTRL_REG3           = 0x22   # 00000000   rw
    GYRO_REGISTER_CTRL_REG4           = 0x23   # 00000000   rw
    GYRO_REGISTER_CTRL_REG5           = 0x24   # 00000000   rw
    GYRO_REGISTER_REFERENCE           = 0x25   # 00000000   rw
    GYRO_REGISTER_OUT_TEMP            = 0x26   #            r
    GYRO_REGISTER_STATUS_REG          = 0x27   #            r
    GYRO_REGISTER_OUT_X_L             = 0x28   #            r
    GYRO_REGISTER_OUT_X_H             = 0x29   #            r
    GYRO_REGISTER_OUT_Y_L             = 0x2A   #            r
    GYRO_REGISTER_OUT_Y_H             = 0x2B   #            r
    GYRO_REGISTER_OUT_Z_L             = 0x2C   #            r
    GYRO_REGISTER_OUT_Z_H             = 0x2D   #            r
    GYRO_REGISTER_FIFO_CTRL_REG       = 0x2E   # 00000000   rw
    GYRO_REGISTER_FIFO_SRC_REG        = 0x2F   #            r
    GYRO_REGISTER_INT1_CFG            = 0x30   # 00000000   rw
    GYRO_REGISTER_INT1_SRC            = 0x31   #            r
    GYRO_REGISTER_TSH_XH              = 0x32   # 00000000   rw
    GYRO_REGISTER_TSH_XL              = 0x33   # 00000000   rw
    GYRO_REGISTER_TSH_YH              = 0x34   # 00000000   rw
    GYRO_REGISTER_TSH_YL              = 0x35   # 00000000   rw
    GYRO_REGISTER_TSH_ZH              = 0x36   # 00000000   rw
    GYRO_REGISTER_TSH_ZL              = 0x37   # 00000000   rw
    GYRO_REGISTER_INT1_DURATION       = 0x38   # 00000000   rw

    #=========================================================================
    # OPTIONAL SPEED SETTINGS
    #-------------------------------------------------------------------------
    GYRO_RANGE_250DPS  = 250
    GYRO_RANGE_500DPS  = 500
    GYRO_RANGE_2000DPS = 2000

    def __init__(self, autorange = False, range = GYRO_RANGE_250DPS, busnum=-1, debug=False):
        self._auto_range, self._range = autorange, range


        # Create _gyro
        self._gyro = Adafruit_I2C.Adafruit_I2C(self.L3GD20_ADDRESS, busnum, debug)
        assert self._gyro.readU8(self.GYRO_REGISTER_WHO_AM_I) in (self.L3GD20_ID, self.L3GD20H_ID)


        # Set CTRL_REG1 (0x20)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        # 7-6  DR1/0     Output data rate                                   00
        # 5-4  BW1/0     Bandwidth selection                                00
        #  3  PD        0 = Power-down mode, 1 = normal/sleep mode          0
        #  2  ZEN       Z-axis enable (0 = disabled, 1 = enabled)           1
        #  1  YEN       Y-axis enable (0 = disabled, 1 = enabled)           1
        #  0  XEN       X-axis enable (0 = disabled, 1 = enabled)           1

        # Reset then switch to normal mode and enable all three channels
        self._gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x00);
        self._gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x0F);

        # Set CTRL_REG2 (0x21)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        # 5-4  HPM1/0    High-pass filter mode selection                    00
        # 3-0  HPCF3..0  High-pass filter cutoff frequency selection      0000

        # Nothing to do ... keep default values
        # --------------------------------------------------------------------

        # Set CTRL_REG3 (0x22)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        #   7  I1_Int1   Interrupt enable on INT1 (0=disable,1=enable)       0
        #   6  I1_Boot   Boot status on INT1 (0=disable,1=enable)            0
        #   5  H-Lactive Interrupt active config on INT1 (0=high,1=low)      0
        #   4  PP_OD     Push-Pull/Open-Drain (0=PP, 1=OD)                   0
        #   3  I2_DRDY   Data ready on DRDY/INT2 (0=disable,1=enable)        0
        #   2  I2_WTM    FIFO wtrmrk int on DRDY/INT2 (0=dsbl,1=enbl)        0
        #   1  I2_ORun   FIFO overrun int on DRDY/INT2 (0=dsbl,1=enbl)       0
        #   0  I2_Empty  FIFI empty int on DRDY/INT2 (0=dsbl,1=enbl)         0

        # Nothing to do ... keep default values
        # ------------------------------------------------------------------

        # Set CTRL_REG4 (0x23)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        #   7  BDU       Block Data Update (0=continuous, 1=LSB/MSB)         0
        #   6  BLE       Big/Little-Endian (0=Data LSB, 1=Data MSB)          0
        # 5-4  FS1/0     Full scale selection                               00
        #                                00 = 250 dps
        #                                01 = 500 dps
        #                                10 = 2000 dps
        #                                11 = 2000 dps
        #   0  SIM       SPI Mode (0=4-wire, 1=3-wire)                       0

        # Adjust resolution if requested
        if self._range == self.GYRO_RANGE_250DPS:
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG4, 0x00)
        elif self._range == self.GYRO_RANGE_500DPS:
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG4, 0x10)
        elif self._range == self.GYRO_RANGE_2000DPS:
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG4, 0x20)
        # ------------------------------------------------------------------

        # Set CTRL_REG5 (0x24)
        # ====================================================================
        # BIT  Symbol    Description                                   Default
        # ---  ------    --------------------------------------------- -------
        #   7  BOOT      Reboot memory content (0=normal, 1=reboot)          0
        #   6  FIFO_EN   FIFO enable (0=FIFO disable, 1=enable)              0
        #   4  HPen      High-pass filter enable (0=disable,1=enable)        0
        # 3-2  INT1_SEL  INT1 Selection config                              00
        # 1-0  OUT_SEL   Out selection config                               00

        # Nothing to do ... keep default values
        # ------------------------------------------------------------------


    def _uint16(self, list, idx):
        n = list[idx] | (list[idx+1] << 8)   # Low, high bytes
        return n if n < 32768 else n - 65536 # 2's complement signed

    def _saturated(self, list):
        """
        Checks if any of the entries in the list has saturated the sensor readings
        :param list:
        :return:
        """

        for x in list:
            if x < -32760 or x > 32760:
                return True
        return False

    def _updateRange(self):
        """
        Try to increase the sensor range

        :return: Boolean. True if the range can be adjusted, False if not
        """
        if self._range == self.GYRO_RANGE_250DPS:
            self._range = self.GYRO_RANGE_500DPS

            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x00);
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x0F);
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG4, 0x10);
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG5, 0x80);
            return True
        elif self._range == self.GYRO_RANGE_500DPS:
            self._range = self.GYRO_RANGE_2000DPS

            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x00);
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x0F);
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG4, 0x20);
            self._gyro.write8(self.GYRO_REGISTER_CTRL_REG5, 0x80);
            return True
        else:
            return False

    def read(self):
        """
        :return:
        """
        list = self._gyro.readList(self.GYRO_REGISTER_OUT_X_L | 0x80, 6)
        reading = (
            self._uint16(list, 0),
            self._uint16(list, 2),
            self._uint16(list, 4))

        if not self._auto_range:
            return reading
        elif self._saturated(reading):
            if self._updateRange():  # If it is possible to increase the range, invalidate the reading
                return None
            else:
                return reading
        else:
            return reading


if __name__ == '__main__':
    pass