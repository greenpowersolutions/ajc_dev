#!/usr/bin/env python3

'''
example code to turn on and off relay 12
dbus-send --system --print-reply --dest=com.gpsl.ModbusRelay /com/gpsl/ModbusRelay com.gpsl.ModbusRelay.toggle_relay int32:12 boolean:true
dbus-send --system --print-reply --dest=com.gpsl.ModbusRelay /com/gpsl/ModbusRelay com.gpsl.ModbusRelay.toggle_relay int32:12 boolean:false
dbus-send --system --print-reply --dest=com.gpsl.ModbusRelay /com/gpsl/ModbusRelay com.gpsl.ModbusRelay.read_relay_state int32:12

#!/usr/bin/env python3

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
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

class ModbusRelayService(dbus.service.Object):
    DEVICE_ADDRESS = 1
    SERIAL_PORT = '/dev/ttyUSB0'

    def __init__(self):
        bus_name = dbus.service.BusName('com.gpsl.ModbusRelay', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/com/gpsl/ModbusRelay')
        self.serial_connection = serial.Serial(self.SERIAL_PORT, 9600)

    @dbus.service.method('com.gpsl.ModbusRelay')
    def toggle_relay(self, relay_number, state):
        if 1 <= relay_number <= 16:
            coil_address = relay_number - 1
            cmd = [self.DEVICE_ADDRESS, 0x05, 0, coil_address, 0, int(state)]
            crc = modbus_crc(cmd)
            cmd.append(crc & 0xFF)
            cmd.append(crc >> 8)

            self.serial_connection.write(bytearray(cmd))
            response = self.serial_connection.read(size=8)

            return len(response) == 8
        else:
            return False

    @dbus.service.method('com.gpsl.ModbusRelay')
    def read_relay_state(self, relay_number):
        if 1 <= relay_number <= 16:
            cmd = [self.DEVICE_ADDRESS, 0x01, 0, 0, 0, 16]
            crc = modbus_crc(cmd[0:6])
            cmd.append(crc & 0xFF)
            cmd.append(crc >> 8)

            self.serial_connection.write(bytearray(cmd))
            response = self.serial_connection.read(size=5 + 2)

            if len(response) >= 5:
                relay_states = response[3:5]
                state = (relay_states[(relay_number - 1) // 8] >> ((relay_number - 1) % 8)) & 0x01
                return bool(state)
            else:
                return None  # Return None if there was an error.
        else:
            return None  # Return None if relay_number is out of range.

DBusGMainLoop(set_as_default=True)
service = ModbusRelayService()
loop = GLib.MainLoop()
loop.run()
'''