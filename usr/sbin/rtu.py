#!/usr/bin/env python3
from pymodbus.client.sync import ModbusSerialClient
import time

# Initialize Modbus client
client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',  # Change to your USB-RS485 device path
    baudrate=9600,       # Adjust baud rate, parity, stop bits as per your device
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

# Connect to the device
client.connect()

# Device address (Slave ID)
DEVICE_ADDRESS = 1

try:
    for _ in range(10):
        # Turn ON coil at address 10 (or 11 considering 1-based indexing)
        result_on = client.write_coil(10, True, unit=DEVICE_ADDRESS)
        if not result_on.isError():
            print("Relay turned ON.")
        else:
            print("Error turning relay ON.")

        # Wait for 2 seconds
        time.sleep(2)

        # Turn OFF coil at address 10 (or 11 considering 1-based indexing)
        result_off = client.write_coil(10, False, unit=DEVICE_ADDRESS)
        if not result_off.isError():
            print("Relay turned OFF.")
        else:
            print("Error turning relay OFF.")

        # Wait for 2 seconds before next iteration
        time.sleep(2)

finally:
    # Close the Modbus connection
    client.close()

