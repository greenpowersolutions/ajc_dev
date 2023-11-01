#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import serial
import time
import sys

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

def send_command(s, relay, action):
    cmd = [0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = 0x01  # Device address
    cmd[2] = 0
    cmd[3] = relay

    if action == "on":
        cmd[1] = 0x05  # Write single coil
        cmd[4] = 0xFF
        cmd[5] = 0
    elif action == "off":
        cmd[1] = 0x05  # Write single coil
        cmd[4] = 0
        cmd[5] = 0
    elif action == "read":
        cmd[1] = 0x01  # Read coil status
        cmd[4] = 0x00
        cmd[5] = 0x10  # Number of coils to read
    else:
        print(f"Invalid action: {action}")
        return

    # Calculate and append CRC
    crc = modbus_crc(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    print(f"Sending command: {cmd}")
    s.write(bytearray(cmd))

    if action == "read":
        response = s.read(5 + 2)  # Assuming 1 byte address, 1 byte function, 1 byte byte-count, 2 bytes of coil statuses (for 16 coils), 2 bytes CRC
        if len(response) == 7:
            byte_count = response[2]
            coil_statuses = response[3:5]  # Two bytes of coil statuses
            if (coil_statuses[0] >> (relay % 8)) & 0x01:
                print(f"Relay {relay} is ON")
            else:
                print(f"Relay {relay} is OFF")
        else:
            print(f"Error reading relay state. Received {len(response)} bytes: {response}")
    else:
        time.sleep(0.2)

    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script_name.py [relay_number] [action(on/off/read)]")
        sys.exit(1)

    relay = int(sys.argv[1])
    action = sys.argv[2]

    if relay < 0 or relay > 15:
        print("Relay number must be between 0 and 15.")
        sys.exit(1)

    try:
        s = serial.Serial("/dev/ttyUSB0", 9600)
        send_command(s, relay, action)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        s.close()
