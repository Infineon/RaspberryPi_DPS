import DPS

from time import sleep


dps368 = DPS.DPS()
try:

        while True:

            scaled_p = dps368.calcScaledPressure()

            scaled_t = dps368.calcScaledTemperature()

            p = dps368.calcCompPressure(scaled_p, scaled_t)

            t = dps368.calcCompTemperature(scaled_t)

            print(f'{p:8.1f} Pa {t:4.1f} C')

            sleep(0.1)

except KeyboardInterrupt:

        pass
