#!/usr/bin/env python3

'''
example code to turn on and off relay 12
dbus-send --system --print-reply --dest=com.gpsl.ModbusRelay /com/gpsl/ModbusRelay com.gpsl.ModbusRelay.toggle_relay int32:12 boolean:true
dbus-send --system --print-reply --dest=com.gpsl.ModbusRelay /com/gpsl/ModbusRelay com.gpsl.ModbusRelay.toggle_relay int32:12 boolean:false
dbus-send --system --print-reply --dest=com.gpsl.ModbusRelay /com/gpsl/ModbusRelay com.gpsl.ModbusRelay.read_relay_state int32:12
'''

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject
from pymodbus.client.sync import ModbusSerialClient
import time

class ModbusRelayService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName('com.gpsl.ModbusRelay', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/com/gpsl/ModbusRelay')

    @dbus.service.method('com.gpsl.ModbusRelay')
    def toggle_relay(self, relay_number, state):
        if 1 <= relay_number <= 16:
            coil_address = relay_number - 1
            client = ModbusSerialClient(
                method='rtu',
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity='N',
                stopbits=1,
                bytesize=8,
                timeout=20
            )
            client.connect()
            DEVICE_ADDRESS = 1
            result = client.write_coil(coil_address, state, unit=DEVICE_ADDRESS)
            client.close()
            return not result.isError()
        else:
            return False

    @dbus.service.method('com.gpsl.ModbusRelay')
    def read_relay_state(self, relay_number):
        if 1 <= relay_number <= 16:
            coil_address = relay_number - 1
            client = ModbusSerialClient(
                method='rtu',
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity='N',
                stopbits=1,
                bytesize=8,
                timeout=20
            )
            client.connect()
            DEVICE_ADDRESS = 1
            result = client.read_coils(coil_address, 1, unit=DEVICE_ADDRESS)
            client.close()

            if not result.isError():
                # Since we're reading only one coil, the result will be a list with one item.
                # Return True if the coil is ON, otherwise return False.
                return result.bits[0]
            else:
                return None  # Return None if there was an error.
        else:
            return None  # Return None if relay_number is out of range.

DBusGMainLoop(set_as_default=True)

service = ModbusRelayService()
loop = GLib.MainLoop()
loop.run()
