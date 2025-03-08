# SPDX-FileCopyrightText: 2020 Mark Raleson
#
# SPDX-License-Identifier: MIT

# Provide readable sensor values and writable settings to connected devices via JSON characteristic.

import time
import random
from ble_json_service import SensorService
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement


# Create BLE radio, custom service, and advertisement.
ble = BLERadio()
service = SensorService()
advertisement = ProvideServicesAdvertisement(service)

# setup sensors
import board
import analogio

# Measure analog moisture levels
# Initialize analog input pins
analog_A0 = analogio.AnalogIn(board.PA0)
analog_A4 = analogio.AnalogIn(board.PA4)

def get_voltage(pin):
    """Convert raw ADC reading to voltage (0 - 3.3V)"""
    return (pin.value * 3.3) / 65535  # 16-bit ADC resolution (0-65535)

def clear_screen():
    """Clears the terminal output"""
    print("\033[2J\033[H", end="")

# Main loop to read and print analog values
while True:
    raw_A0 = analog_A0.value  # Raw ADC value (0-65535)
    voltage_A0 = get_voltage(analog_A0)  # Convert to voltage

    raw_A4 = analog_A4.value  # Raw ADC value (0-65535)
    voltage_A4 = get_voltage(analog_A4)  # Convert to voltage

    print(f"A0: {raw_A0} ({voltage_A0:.2f}V), A4: {raw_A4} ({voltage_A4:.2f}V)")
    time.sleep(.1)  # Wait 1 second before next reading
    clear_screen()

# Function to get some fake weather sensor readings for this example in the desired unit.
def measure(unit):
    temperature = random.uniform(0.0, 10.0)
    humidity = random.uniform(0.0, 100.0)
    if unit == "fahrenheit":
        temperature = (temperature * 9.0 / 5.0) + 32.0
    return {"timestamp": time.monotonic(),"temperature": temperature, "humidity": humidity}


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
