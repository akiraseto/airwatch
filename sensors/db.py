#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""取得データを保存."""

import os

from pymongo import MongoClient


class MongoDB:
    """ダイキンセンサーDB."""

    def __init__(self):
        """イニシャライザ."""
        db_host = os.environ['DB_HOST']
        db_port = 27017
        self.client = MongoClient(db_host, db_port)

        self.db = None

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

        Returns
        -------
        dict
            最新データ1つ

        """
        db_col = self.db.get_collection(periods)
        res = db_col.find_one(sort=[('timestamp', -1)],
                              projection={'_id': 0, })
        return res
