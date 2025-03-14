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
from mysensors import SoilTempAndMoistureSensor

# Create BLE radio, custom service, and advertisement.
ble = BLERadio()
service = SensorService()
advertisement = ProvideServicesAdvertisement(service)

# Create sensor objects
moist1_sens = MoistureSensor(board.PA0)
comm_port = busio.I2C(board.PD0, board.PD1)
uv_sens = UVSensor(comm_port, 0x74)
soil_sens = SoilTempAndMoistureSensor(comm_port, 0x36)

def measure_sensors():
    soil_temp_val = soil_sens.getFTemp()
    uva = uv_sens.getUvaPercentage()
    temp = uv_sens.getFTemp()
    moisture_val = moist1_sens.getMoistPercentage()

    sensor_data_dict = {"moist": moisture_val, "uva": uva, "air_temp": temp, "soil_temp": soil_temp_val}
    sensor_unit_dict = {"moist": "%", "uva": "%", "air_temp": "F", "soil_temp": "F"}
    return {"sensor_data": sensor_data_dict, "sensor_units": sensor_unit_dict}

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
