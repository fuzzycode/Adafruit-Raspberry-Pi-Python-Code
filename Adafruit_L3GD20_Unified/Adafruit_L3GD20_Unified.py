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

if __name__ == '__main__':
    pass