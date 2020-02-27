import DPS

from time import sleep

dps422 = DPS.DPS422()

#print(dps422.measureBothOnce())

temperature, pressure = dps422.measureBothOnce()

print("Temperature in celsius: ", temperature)

print("Pressure in pascals: ", pressure)