#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""データベース設定."""

from pymongo import MongoClient


class MongoDB:
    """ダイキンセンサーDB."""

    def __init__(self):
        """イニシャライザ."""
        db_host = 'db'
        db_port = 27017

        self.client = MongoClient(db_host, db_port)
