#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""取得データを保存."""

from pymongo import MongoClient


class MongoDB:
    """ダイキンセンサーDB."""

    def __init__(self):
        """イニシャライザ."""
        db_host = 'db'
        db_port = 27017
        db_name = 'airwatch'

        client = MongoClient(db_host, db_port)
        self.db = client[db_name]
