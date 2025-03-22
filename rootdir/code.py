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

def scanI2C(comm_port):
    while not comm_port.try_lock():
        pass  # Wait until I2C bus is available

    try:
        addresses = comm_port.scan()  # Get list of I2C device addresses
        if addresses:
            print("Found I2C devices at addresses:")
            for address in addresses:
                print(f"0x{address:02X}")  # Print address in hex format
        else:
            print("No I2C devices found.")
    finally:
        comm_port.unlock()  # Release I2C bus

# Create BLE radio, custom service, and advertisement.
ble = BLERadio()
service = SensorService()
advertisement = ProvideServicesAdvertisement(service)

print(ble.tx_power)

# Create sensor objects
moist1_sens = MoistureSensor(board.PA0)
comm_port1 = busio.I2C(board.PD0, board.PD1)

scanI2C(comm_port1)

uv_sens = UVSensor(comm_port1, 0x74)
soil_sens = SoilTempAndMoistureSensor(comm_port1, 0x36)

UPDATE_INTERVAL_S = 1.3*60

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
    ble.start_advertising(advertisement, None, .5)
   
    print("Waiting for connection...")
    while not ble.connected:
        pass

    print("Connected")
    while ble.connected:
        settings = service.settings
        measurement = measure_sensors()
        service.sensors = measurement
        print("Sensors: ", measurement)
        time.sleep(UPDATE_INTERVAL_S)

    print("Disconnected")
