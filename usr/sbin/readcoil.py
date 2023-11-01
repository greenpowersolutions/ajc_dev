#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import serial
import time

s = serial.Serial("/dev/ttyUSB0", 9600)
s.close()

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

# Open serial port
s = serial.Serial("/dev/ttyUSB0", 9600)

# Function to read the state of all 16 relays
def read_relay_states():
    # Construct the command to read 16 coils starting from address 0
    cmd = [0x01,  # Device address
           0x01,  # Function code for Read Coils
           0x00,  # Starting address Hi
           0x00,  # Starting address Lo
           0x00,  # Quantity of coils Hi
           0x10]  # Quantity of coils Lo (16 coils)

    # Calculate CRC
    crc = modbus_crc(cmd)
    cmd.append(crc & 0xFF)
    cmd.append(crc >> 8)

    # Send command
    s.write(bytearray(cmd))

    # Wait for response
    time.sleep(0.2)

    # Read response
    response = s.read(5)

    return response


response = read_relay_states()
print(response)


# Close serial port
s.close()
