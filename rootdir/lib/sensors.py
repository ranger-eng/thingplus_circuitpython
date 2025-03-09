import iorodeo_as7331
import time
import board
import analogio

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

class MoistureSensor(analogio.AnalogIn):
    def __init__(self, pin):
        super().__init__(pin)

    rail_voltage = 3.3
    num_ADC_vals = 65535 # 16-bit ADC resolution

    def getVoltage(self):
        """Get voltage value from sensor"""
        return (self.value * self.rail_voltage / self.num_ADC_vals)
