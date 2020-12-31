#!/usr/bin/env python
"""
This code is inspired by the bme280wx implementation at: https://gitlab.com/wjcarpenter/bme280wx/-/blob/master/bin/user/bme280wx.py
bme280wx
"""
import smbus2
import weewx
from weewx.engine import StdService
import weeutil

from bme280logger import log, LogLevel
from bme280config import BME280Config
from bme280reader import BME280Reader


class BME280ConfigWeewx(BME280Config):

    def __init__(self, data: dict = None):
        super().__init__(data)

        # Add Weewx specific configuration
        self.defaultUnits: str = "US"
        self.temperatureKeys: list = ["inTemp"]
        self.temperatureRequiredValues: list = []
        self.humidityKeys: list = ["inHumidity"]
        self.humidityRequiredValues: list = []
        self.pressureKeys: list = ["pressureKeys"]
        self.pressureRequiredValues: list = ["'outTemp'"]

    def load(self, data: dict) -> bool:
        super().load(data)

        # Load the Weewx specific configuration
        self.defaultUnits = data.get("units", self.defaultUnits).upper()
        self.temperatureKeys = data.get(
            "temperatureKeys", self.temperatureKeys)
        self.teperatureRequiredValues = data.get(
            "temparatureRequiredValues", self.temperatureRequiredValues)
        self.humidityKeys = data.get("humidityKeys", self.humidityKeys)
        self.humidityRequiredValues = data.get(
            "humidityRequiredValues", self.humidityRequiredValues)
        self.pressureKeys = data.get("pressureKeys", self.pressureKeys)
        self.pressureRequiredValues = data.get("pressureRequiredValues")


class FT232BME280(StdService):

    def __init__(self, engine, config: dict):
        super(FT232BME280, self).__init__(engine, config)
        bme280Data: dict = config.get('FT232BME280', None)
        log(LogLevel.INFO, 'bme280 configuration %s' % bme280Data)
        self.bme280Config = BME280ConfigWeewx()
        self.bme280Config.load(bme280Data)

        self.bme280Reader = BME280Reader(self.bme280Config)
        self.bme280Reader.connect()

        # Do one initial read as the first values returned from the sensor
        # are often bogus
        self.bme280Reader.read()

        # This is last to make sure all the other stuff is ready to go
        # (avoid race condition)
        self.bind(weewx.NEW_LOOP_PACKET, self.newLoopPacket)

    def newLoopPacket(self, event):
        packet = event.packet

        if not self.bme280Reader.connected():
            self.bme280Reader.connect()

        dataRecord = self.bme280Reader.read()
        log(LogLevel.INFO, 'BME280 data %s' % dataRecord.string())

        if dataRecord is None:
            return

        # use packet units if available
        if 'usUnits' in packet:
            converter = weewx.units.StdUnitConverters[packet['usUnits']]
        else:
            converter = weewx.units.StdUnitConverters[self.bme280Config.defaultUnits]

        if all(mustHave in packet for mustHave in self.bme280Config.pressureRequiredValues) or len(self.bme280Config.pressureRequiredValues) == 0:
            pressurePA = (dataRecord.pressure / 100, 'hPa', 'group_pressure')
            converted = converter.convert(pressurePA)
            for key in self.bme280Config.pressureKeys:
                packet[key] = converted[0]

        if all(mustHave in packet for mustHave in self.bme280Config.temperatureRequiredValues) or len(self.bme280Config.temperatureRequiredValues) == 0:
            temperatureC = (dataRecord.temperature,
                            'degree_C', 'group_temperature')
            converted = converter.convert(temperatureC)
            for key in self.bme280Config.temperatureKeys:
                packet[key] = converted[0]

        if all(mustHave in packet for mustHave in self.bme280Config.humidityRequiredValues) or len(self.bme280Config.humidityRequiredValues) == 0:
            humidityPCT = (dataRecord.humidity, 'percent', 'group_percent')
            converted = converter.convert(humidityPCT)
            for key in self.bme280Config.humidityKeys:
                packet[key] = converted[0]

        log(LogLevel.DEBUG, "BME280 Packet: %s" % packet)
