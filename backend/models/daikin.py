#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダイキンセンサーモデル."""

from db import MongoDB


class Daikin(MongoDB):
    """ダイキンデータDB."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        db_name = 'daikin'
        self.db = self.client[db_name]
