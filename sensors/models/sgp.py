#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SGP30 空気品質センサー."""

import logging
from datetime import datetime

import adafruit_sgp30
import board
import busio

from db import MongoDB


class Sgp(MongoDB):
    """SGP30 IO."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        # センサー
        i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.sensor = adafruit_sgp30.Adafruit_SGP30(i2c_bus)

        # MongoDB
        db_name = 'sgp'
        self.db = self.client[db_name]

    def get_sensor(self):
        """Get センサー値.

        Returns
        -------
        dict
            各センサー値

        """
        try:
            co2, tvoc = self.sensor.iaq_measure()
            h2, ethanol = self.sensor.raw_measure()

            return {
                'co2': co2,
                'tvoc': tvoc,
                'h2': h2,
                'ethanol': ethanol,
                'timestamp': datetime.now()
            }

        except Exception as e:
            logging.error('SensorError: {}'.format(e))
            return None
