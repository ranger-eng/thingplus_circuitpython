# SPDX-FileCopyrightText: 2020 Mark Raleson
#
# SPDX-License-Identifier: MIT

# Provide readable sensor values and writable settings to connected devices via JSON characteristic.

import time
import random
from ble_json_service import SensorService
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

import board
import busio
from mysensors import MoistureSensor
from mysensors import UVSensor

# Create BLE radio, custom service, and advertisement.
ble = BLERadio()
service = SensorService()
advertisement = ProvideServicesAdvertisement(service)

# Create sensor objects
moist1_sens = MoistureSensor(board.PA0)
moist2_sens = MoistureSensor(board.PA4)
comm_port = busio.I2C(board.PD0, board.PD1)
uv_sens = UVSensor(comm_port, 0x74)

def measure_sensors():
    moist1_val = moist1_sens.getValue()
    moist2_val = moist2_sens.getValue()
    uva, uvb, uvc, temp = uv_sens.values
    sensor_data_dict = {"moist1": moist1_val, "moist2": moist2_val, "uva": uva, "uvb": uvb, "uvc": uvc, "air_temp": temp}
    sensor_unit_dict = {"moist1": "V", "moist2": "V", "uva": "%", "uvb": "%", "uvc": "%", "air_temp": "C"}
    return {"sensor_data": sensor_data_dict, "sensor_unit": sensor_unit_dict}

# Advertise until another device connects, when a device connects, provide sensor data.
while True:
    print("Advertise services")
    ble.stop_advertising()  # you need to do this to stop any persistent old advertisement
    ble.start_advertising(advertisement)

    print("Waiting for connection...")
    while not ble.connected:
        pass

    print("Connected")
    while ble.connected:
        settings = service.settings
        measurement = measure_sensors()
        service.sensors = measurement
        print("Sensors: ", measurement)
        time.sleep(0.25)

    print("Disconnected")
