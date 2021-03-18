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
        humi, temp = DHT.read_retry(DHT.DHT11, self.PIN)
        return {
            'humi': humi,
            'temp': temp,
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
