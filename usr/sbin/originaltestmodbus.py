#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import serial
import time

# Modbus CRC16 calculation function
def modbus_crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

s = serial.Serial("/dev/ttyUSB0", 9600)
cmd = [0, 0, 0, 0, 0, 0, 0, 0]

cmd[0] = 0x01  # Device address
cmd[1] = 0x05  # Command

while True:
    for i in range(16):
        cmd[2] = 0
        cmd[3] = i
        cmd[4] = 0xFF
        cmd[5] = 0
        crc = modbus_crc(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        print(cmd)
        s.write(bytearray(cmd))
        time.sleep(0.2)

    for i in range(16):
        cmd[2] = 0
        cmd[3] = i
        cmd[4] = 0
        cmd[5] = 0
        crc = modbus_crc(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        print(cmd)
        s.write(bytearray(cmd))
        time.sleep(0.2)
