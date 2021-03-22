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
            res[db_name] = self.get_data(params)

        return res
