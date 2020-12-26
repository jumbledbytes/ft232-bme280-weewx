# install for ft232bme280 weewx extension

from setup import ExtensionInstaller


def loader():
    return FT232BME280Installer()


class FT232BME280Installer(ExtensionInstaller):
    def __init__(self):
        super(FT232BME280Installer, self).__init__(
            version="1.0",
            name='FT232BME280',
            description='Add bme280 sensor connected to FT232 breakout board readings to loop packet data',
            author="Jeff",
            author_email="jeff@jumbledbytes.com",
            data_services='user.ft232bme280.FT232BME280',
            config={
                'FT232BME280': {
                    'deviceURI': 'ftdi://ftdi:232h/1',
                    'busFrequency': 100000,
                    'usUnits': 'US',
                    'temperatureKeys': 'inTemp',
                    'temperatureRequiredValues': '',
                    'pressureKeys': 'pressure',
                    'pressureRequiredValues': 'outTemp',
                    'humidityKeys': 'inHumidity',
                    'humidityRequiredValues': ''
                }
            },
            files=[('bin/user', ['bin/user/ft232bme280.py'])]
        )
