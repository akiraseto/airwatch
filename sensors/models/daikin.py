#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダイキン."""

from datetime import datetime
from io import StringIO

import requests
from dotenv import dotenv_values

from db import MongoDB


class Daikin(MongoDB):
    """Daikin IO."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        self.sensor = {
            'uri': 'http://192.168.0.10',
            'param': '/cleaner/get_sensor_info'
        }

        col_name = 'daikin'
        self.db_col = self.db.get_collection(col_name)

    def get_sensor(self):
        """Get センサー."""
        res = requests.get(self.sensor['uri'] + self.sensor['param'])
        return res.text

    def insert_data(self, data):
        """
        センサーデータを保存.

        Parameters
        ----------
        data : str
            センサーデータ

        Returns
        -------
        None

        """
        insert_data = {}

        list_split_data = data.split(',')

        for val in list_split_data:
            val = StringIO(val)
            val.seek(0)
            parsed_val = dotenv_values(stream=val)

            if 'ret' not in parsed_val:
                for index, value in parsed_val.items():
                    insert_data[index] = float(value)

        insert_data['timestamp'] = datetime.now()

        self.db_col.insert_one(insert_data)
