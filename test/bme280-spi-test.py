#!/usr/bin/env python3
# file: bme280-monitor.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2018-04-22T20:56:36+0200
# Last modified: 2018-11-10T16:39:28+0100
"""
Monitoring program for the Bosch BME280 temperature, pressure and humidity sensor.
The sensor is connected to the computer via an FT232H using SPI.

Connect 5V and ground from the FT232H to their respective pins on the BMP280.
Then connect D0 to SCK, D1 to SDI, D2 to SDO and e.g. D3 to CS.
You can use the -c or --cs option to choose another chip select line.
"""

from datetime import datetime
from enum import IntEnum
import argparse
import sys
import time

from pyftdi.spi import SpiController
from bme280spi import BME280spi

from bme280config import BME280Config
from bme280reader import BME280Reader
from ft232h import FT232Ports

__version__ = '0.1'


def main(argv):
    """
    Entry point for bme280-monitor.py

    Arguments:
        argv: command line arguments
    """

    args = process_arguments(argv)
    bme280Data:  dict = {}
    bme280Data["deviceURI"] = args.device
    bme280Data["chipSelect"] = args.cs

    config = BME280Config(bme280Data)
    bme280Reader = BME280Reader(config)

    print("Connecting to BME280 at %s" % config.deviceURI)
    if not bme280Reader.connect():
        print("Unable to connect to BME280 sensor. Exiting.")
        sys.exit(1)

    try:
        # Ignore the first reading
        bme280Reader.read()
        count = 0
        while True:
            dataRecord = bme280Reader.read()
            line = '{} {:.2f} {:.0f} {:.2f}'.format(
                dataRecord.time, dataRecord.temperature, dataRecord.pressure, dataRecord.humidity
            )
            print(f"{count}: {line}")
            count += 1
            time.sleep(args.interval)
    except KeyboardInterrupt:
        sys.exit(1)


def process_arguments(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-c',
        '--cs',
        default="D3",
        type=str,
        help='FT232 pin to use for SPI chip select (default D3, range D3 - D7).'
    )
    parser.add_argument(
        '-d',
        '--device',
        default='ftdi://ftdi:232h/1',
        type=str,
        help='FT232 device (default "ftdi://ftdi:232h/1"). '
        'See the pyftdi documentation for more information about the URL scheme.'
    )
    parser.add_argument(
        '-f',
        '--frequency',
        default=100000,
        type=int,
        help='SPI bus requency in Hz (default 100000 Hz, must be >91 Hz and <6 MHz).'
    )
    parser.add_argument(
        '-i',
        '--interval',
        default=5,
        type=int,
        help='interval between measurements (≥5 s, default 5 s).'
    )
    parser.add_argument('-v', '--version',
                        action='version', version=__version__)

    args = parser.parse_args(argv)
    return args


if __name__ == '__main__':
    main(sys.argv[1:])
