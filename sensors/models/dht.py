#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DHT 温度湿度センサー."""

from datetime import datetime

import Adafruit_DHT as DHT

from db import MongoDB


class Dht(MongoDB):
    """DHT IO."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        # センサー
        self.PIN = 20

        # MongoDB
        db_name = 'dht'
        self.db = self.client[db_name]

    def get_sensor(self):
        """Get センサー値.

        Returns
        -------
        dict
            各センサー値

        """
        try:
            humi, temp = DHT.read_retry(DHT.DHT11, self.PIN)
            return {
                'temp': temp,
                'humi': humi,
                'timestamp': datetime.now()
            }

        except Exception as e:
            print('Error:', e)
            return None
