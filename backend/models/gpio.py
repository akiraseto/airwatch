#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GPIOセンサーモデル."""

from db import MongoDB


class Gpio(MongoDB):
    """GPIOデータDB."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        self.db = None
        self.db_name_list = [
            'bmp',
            'dht',
            'sgp',
        ]

    def get_sensors_data(self, params):
        """sensor群のデータを一括取得."""
        res = {}

        for db_name in self.db_name_list:
            self.db = self.client[db_name]
            data = self.get_data(params)
            res.update(data)

        res['temp'] = [round((x + y) / 2, 1) for (x, y) in
                       zip(res['btemp'], res['dtemp'])]
        res.pop('btemp')
        res.pop('dtemp')

        return res
