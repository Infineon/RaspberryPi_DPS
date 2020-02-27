import DPS

from time import sleep


dps310 = DPS.DPS()


temperature= dps310.measureTemperatureOnce()


pressure= dps310.measurePressureOnce()


print(f'{temperature:4.1f}C {pressure:8.1f}Pa')
