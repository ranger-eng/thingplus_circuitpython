# SPDX-FileCopyrightText: 2020 Mark Raleson
#
# SPDX-License-Identifier: MIT

# Provide readable sensor values and writable settings to connected devices via JSON characteristic.

import time
import random
from ble_json_service import SensorService
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement



# setup sensors
import board
import busio
import sensors

# Measure analog moisture levels
# Initialize analog input pins
moistSensor1 = sensors.MoistureSensor(board.PA0)
moistSensor2 = sensors.MoistureSensor(board.PA4)
comm_port = busio.I2C(board.PD0, board.PD1)

# Create BLE radio, custom service, and advertisement.
ble = BLERadio()
service = SensorService()
advertisement = ProvideServicesAdvertisement(service)

uvSensor = sensors.UVSensor(comm_port, 0x74)

def clear_screen():
    """Clears the terminal output"""
    print("\033[2J\033[H", end="")

def measure():
    m1_val = moistSensor1.getVoltage()
    m2_val = moistSensor2.getVoltage()
    uva_val, _, _, temp_val = uvSensor.values
    return {"moisture1": m1_val, "moisture2": m2_val, "uva": uva_val, "air_temp": temp_val}

# Main loop to read and print analog values
while True:
    print("Advertise services")
    ble.stop_advertising()  # you need to do this to stop any persistent old advertisement
    ble.start_advertising(advertisement)

    print("Waiting for connection...")
    while not ble.connected:
        pass

    print("Connected")
    while ble.connected:
        measurement = measure()
        service.sensors = measurement
        print("Characteristics: ", service.bleio_characteristics)
        print("Sensors: ", service.sensors)
        time.sleep(3)

    print("Disconnected")

# Advertise until another device connects, when a device connects, provide sensor data.
while True:
    print("Advertise services")
    ble.stop_advertising()  # you need to do this to stop any persistent old advertisement
    ble.start_advertising(advertisement)
    print(advertisement.match_prefixes)

    print("Waiting for connection...")
    while not ble.connected:
        pass

    print("Connected")
    while ble.connected:
        settings = service.settings
        measurement = measure(settings.get("unit", "celsius"))
        service.sensors = measurement
        print("Settings: ", settings)
        print("Sensors: ", measurement)
        time.sleep(0.25)

    print("Disconnected")
