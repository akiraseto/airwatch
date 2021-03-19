#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BMP 室温気圧センサー."""

import logging
from datetime import datetime

import Adafruit_BMP.BMP085 as BMP085

from db import MongoDB


class Bmp(MongoDB):
    """BMP180 IO."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        # センサー
        self.sensor = BMP085.BMP085()

        # MongoDB
        db_name = 'bmp'
        self.db = self.client[db_name]

    def get_sensor(self):
        """Get センサー値.

        Returns
        -------
        dict
            各センサー値

        """
        try:
            return {
                'temp': self.sensor.read_temperature(),
                'press': self.sensor.read_pressure(),
                'alti': self.sensor.read_altitude(),
                'sealev': self.sensor.read_sealevel_pressure(),
                'timestamp': datetime.now()
            }

        except Exception as e:
            logging.error('SensorError: {}'.format(e))
            return None
