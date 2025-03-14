import iorodeo_as7331
import time
import board
import analogio
import adafruit_seesaw.seesaw

UVA_MAX_VAL = 25

def cToF(cVal):
    fVal = (cVal * 9/5) + 32
    return fVal

class UVSensor(iorodeo_as7331.AS7331):
    def __init__(self, i2c_bus, address):
        super().__init__(i2c_bus, address)

        self.gain = iorodeo_as7331.GAIN_512X
        self.integration_time = iorodeo_as7331.INTEGRATION_TIME_128MS

        print(f'chip id:            {self.chip_id}')
        print(f'device state:       {self.device_state_as_string}')
        print(f'gain_as_string:     {self.gain_as_string}')
        print(f'integration_time:   {self.integration_time_as_string}')
        print(f'divider enabled:    {self.divider_enabled}')
        print(f'divider:            {self.divider}')
        print(f'power_down_enable:  {self.power_down_enable}')
        print(f'standby state:      {self.standby_state}')
        print(f'gain:               {self.gain_as_string}')
        print('-'*60)

        time.sleep(2)

    def getUvaPercentage(self):
        uva, _, _, _ = self.values
        uvaPercent = uva/UVA_MAX_VAL*100
        return uvaPercent

    def getFTemp(self):
        _, _, _, cTemp = self.values
        fTemp = cToF(cTemp)
        return fTemp

class MoistureSensor(analogio.AnalogIn):
    def __init__(self, pin):
        super().__init__(pin)

    rail_voltage = 3.3
    num_ADC_vals = 65535 # 16-bit ADC resolution

    def getMoistPercentage(self):
        voltageVal = self.value * self.rail_voltage / self.num_ADC_vals
        return voltageVal/2.6*100

class SoilTempAndMoistureSensor(adafruit_seesaw.seesaw.Seesaw):
    def __init__(self, i2c_bus, addr=0x48):
        super().__init__(i2c_bus, addr)

    def getFTemp(self):
        cTemp = self.get_temp()
        fTemp = cToF(cTemp)
        return fTemp

    def getMoisturePercentage(self):
        moistVal = self.moisture_read()
        moistValPercentage = moistVal
        return moistValPercentage
