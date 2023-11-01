#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import serial
import time
import argparse

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

def set_relay_state(serial_port, relay_num, action):
    cmd = [0] * 8
    cmd[0] = 0x01  # Device address

    if action == "on":
        cmd[1] = 0x05  # Command for turning a single relay on
    else:
        cmd[1] = 0x00  # Command for turning a single relay off

    cmd[2] = 0
    cmd[3] = relay_num  # Relay number

    crc = modbus_crc(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8

    serial_port.write(bytearray(cmd))
    response = serial_port.read(size=8)  # Read response from the device

    # You can add any validation or confirmation checks based on the response

def main():
    parser = argparse.ArgumentParser(description="Control relay states.")
    parser.add_argument("-a", "--action", choices=["on", "off"], required=True, help="Action to perform (on/off)")
    parser.add_argument("-r", "--relay", type=int, choices=range(16), required=True, help="Relay number (0-15)")
    args = parser.parse_args()

    with serial.Serial("/dev/ttyUSB0", 9600) as s:
        set_relay_state(s, args.relay, args.action)

if __name__ == "__main__":
    main()
