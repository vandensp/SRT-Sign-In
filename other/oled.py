#!/usr/bin/env python3
import smbus
import time
bus = smbus.SMBus(1)
address1 = 0x78
while True:
    temp = bus.read_byte_data(address1, 0)
    print(str(temp) + " " + str(temp2), end = "\r")
    time.sleep(0.25)