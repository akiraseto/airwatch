#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GPIOセンサーモデル."""

from db import MongoDB


class Gpio(MongoDB):
    """GPIOデータDB."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        self.db_name_bmp = 'bmp'
        self.db_name_dht = 'dht'
        self.db = None

    def get_bmp_data(self, params):
        """BMP180のデータを取得."""
        self.db = self.client[self.db_name_bmp]

        res = self.get_data(params)
        return res

    def get_dht_data(self, params):
        """DHTのデータを取得."""
        self.db = self.client[self.db_name_dht]

        res = self.get_data(params)
        return res
