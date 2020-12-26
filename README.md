# Overview

This is a weewx extension that adds support for the BME280 sensor connected to weewx by a FT232 breakout board.

The extension allows custom weather stations to be built using components that do not provide a set of I2C or GPIO pins to connect the Bosche BME280 pressure, temperature, and humidity environmental sensor.

This project is inspired by https://gitlab.com/wjcarpenter/bme280wx/-/tree/master, but does not use that package as it requires an I2C interface to function. This package re-purposes the approach to use an SPI interface and support the BME280 sensor over USB.

# Prerequisites

As a WeeWx extension this package is dependent upon WeeWx. However this package is developed using Python3 and likely will not work (and is not tested) using Python2.

This package is tested using versions of WeeWx > 4.1 using Python3.

This packages is dependent upon [ft232-bme280](https://github.com/jumbledbytes/ft232-bme280)

## Installing the Dependencies

- Install WeeWx per the excellent instructions and documentation provided on the WeeWx website: http://www.weewx.com/docs/usersguide.htm#installing

- Install the [ft232-bme280](https://github.com/jumbledbytes/ft232-bme280) python package. Follow the installation and validation instructions provided with the `ft232-bme280` package.

# Installation

## Option 1: Install the latest version from GitHub

Download the latest version of this package from GitHub:

Link TBD

Run the `wee_extension` installation:

```
wee_extension --install <downloaded_package>
```

## Option 2: Install from source

Clone this repo to your local system make an archive of the repo:

```
git clone https://github.com/jumbledbytes/ft232-bme280-weewx.git
```

then

```
tar cvzf ft232-bme280-weewx.tgz ft232-bme280-weewx
wee_extension --install ft232-bme280-weewx.tgz
```

After the extension is installed verify your weewx.conf configuration file and restart weewx:
