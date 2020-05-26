[![PyPI](https://img.shields.io/pypi/v/DigitalPressureSensor.svg)](https://pypi.org/project/DigitalPressureSensor/)      [![Gitter](https://badges.gitter.im/MakerConerFor_DPS/community.svg)](https://gitter.im/MakerConerFor_DPS/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Introduction
============

Python driver for Infineon Digital Barometric Air Pressure Sensor(DPS). This single driver is compatible with all the different versions of S2GO Digital Barometric Air Pressure Sensor from Infineon. 

Different versions of DPS-
---------------------------
* [DPS310](https://github.com/Infineon/DPS310-Pressure-Sensor) The barometric pressure sensors DPS310 offers excellent pressure noise performance and high stability with temperature. [Product](https://www.infineon.com/cms/en/product/sensor/pressure-sensors/absolute-pressure-sensors-map-bap/dps310/)
* [DPS368](https://github.com/Infineon/DPS368-Library-Arduino)  DPS368 is a miniaturized digital barometric air pressure sensor with ultra-high precision (±2 cm) and a low current consumption, capable of measuring both pressure and temperature. Due to its robust package, it can withstand 50 m under water for one hour (IPx8). [Product](https://www.infineon.com/cms/en/product/sensor/pressure-sensors/absolute-pressure-sensors-map-bap/dps368/)
* [DPS422]() The DPS422 is a miniaturized digital barometric air pressure and temperature sensor with high accuracy and low current consumption. Pressure sensing is carried out using a capacitive sensor element, guaranteeing high accuracy over temperature. [Product](https://www.infineon.com/cms/en/product/sensor/pressure-sensors/absolute-pressure-sensors-map-bap/dps422/)

Dependencies
============

This driver depends on:

* python version 3 and above
* [SMBus](https://github.com/kplindegaard/smbus2)

Please ensure all dependencies are resolved before proceeding further.

Steps for installation
----------------------

Supported hardware --> Raspberry pi Zero/3/3B+/4B

* Update apt

```

sudo apt update

```


* Enable i2c (Interfacing options menu and then I2C enable). For detailed steps see this [article](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/).

```

sudo raspi-config

```


* Install pip3

```

sudo apt install python3-pip

```


* Install smbus

```

pip3 install smbus
sudo apt-get install -y python-smbus i2c-tools

```

Installing from PyPI
--------------------

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver from [PyPI](https://pypi.org/)

For current user:
```

pip3 install DigitalPressureSensor

```

To install system-wide (this may be required in some cases):
```

sudo pip3 install DigitalPressureSensor

```

Connection diagram:
-------------------
<img src="https://github.com/Infineon/Assets/blob/master/Pictures/RPi_Connection_DPS.PNG" width=550 >  

| Raspberry Pi | DPS |
| :---: |:---:|
| 3.3V | 3V3 |
| GND | GND |
| BCM 2 (pin3) | SDA |
| BCM 3 (pin 5) | SCL |


**Note-** Connection diagram given with DPS310 and Raspberry pi is just for reference, all the three versions of DPS will be connected in the same way with any of the Raspberry pi.




* Clone the Github repository or download the .zip, unzip it, go to examples folder and run the sample code.

