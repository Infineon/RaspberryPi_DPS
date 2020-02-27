import DPS

from time import sleep


dps368 = DPS.DPS()


temperature= dps368.measureTemperatureOnce()


pressure= dps368.measurePressureOnce()


print(f'{temperature:4.1f}C {pressure:8.1f}Pa')
