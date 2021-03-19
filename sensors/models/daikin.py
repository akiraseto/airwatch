#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダイキン."""

import logging
import os
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

        # センサー
        self.sensor = {
            'uri': os.environ['DAIKIN_URI'],
            'param': '/cleaner/get_sensor_info'
        }

        # MongoDB
        db_name = 'daikin'
        self.db = self.client[db_name]

    def get_sensor(self):
        """Get センサー値.

        Returns
        -------
        dict
            各センサー値

        """
        try:
            res = requests.get(self.sensor['uri'] + self.sensor['param'])
            list_split_data = res.text.split(',')

            res_data = {}
            for val in list_split_data:
                val = StringIO(val)
                val.seek(0)
                parsed_val = dotenv_values(stream=val)

                if 'ret' not in parsed_val:
                    for index, value in parsed_val.items():
                        res_data[index] = float(value)

            res_data['timestamp'] = datetime.now()

            return res_data

        except Exception as e:
            logging.error('SensorError: {}'.format(e))
            return None
