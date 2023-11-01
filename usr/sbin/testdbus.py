#!/usr/bin/env python3
import dbus

# Connect to the system bus
bus = dbus.SystemBus()

# Function to get the relay state
def get_relay_state(relay_number):
    # Access the Victron D-Bus service.
    victron_service = bus.get_object('com.victronenergy.system', f'/Relay/{relay_number-1}')

    # Create an interface to interact with the service
    iface = dbus.Interface(victron_service, 'com.victronenergy.BusItem')

    # Call the GetValue method to get the relay state
    relay_state = iface.GetValue()

    return relay_state.get('State')

# Get the state of Relay 1 and Relay 2
relay1_state = get_relay_state(1)
relay2_state = get_relay_state(2)

# Print the relay statuses
print("Relay 1 Status:", relay1_state)
print("Relay 2 Status:", relay2_state)