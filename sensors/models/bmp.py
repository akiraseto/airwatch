#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BMP 室温気圧センサー."""

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
        return {
            'temp': self.sensor.read_temperature(),
            'press': self.sensor.read_pressure(),
            'alti': self.sensor.read_altitude(),
            'sealev': self.sensor.read_sealevel_pressure(),
            'timestamp': datetime.now()
        }

    def insert_data(self, periods, data):
        """
        センサーデータを保存.

        Parameters
        ----------
        periods : str
            'minute','hour', 'day', 'week'
        data : dict
            センサーデータ

        Returns
        -------
        None

        """
        db_col = self.db.get_collection(periods)
        db_col.insert_one(data)

    def find_latest(self, periods):
        """
        DBから最新データを1つ取得.

        Parameters
        ----------
        periods : str
            'minute','hour', 'day', 'week'
        data : dict
            センサーデータ

        Returns
        -------
        dict
            最新データ1つ

        """
        db_col = self.db.get_collection(periods)
        res = db_col.find_one(sort=[('timestamp', -1)],
                              projection={'_id': 0, })
        return res
