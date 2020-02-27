import DPS

from time import sleep

dps422 = DPS.DPS422()

try:
    while True:

        temperature, pressure = dps422.measureBothOnce()

        #print(dps422.measureBothOnce())

        print("Temperature in celsius: ", temperature)

        print("Pressure in pascals: ", pressure)

        sleep(0.5)

except KeyboardInterrupt:
    pass

