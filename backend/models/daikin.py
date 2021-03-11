#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダイキンセンサーモデル."""

from datetime import datetime, timedelta

import pandas as pd

from db import MongoDB


class Daikin(MongoDB):
    """ダイキンデータDB."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        db_name = 'daikin'
        self.db = self.client[db_name]

    def get_data(self, params, record_limit=100):
        """
        データを取得.

        Parameters
        ----------
        params : dict
            検索パラメーター
        record_limit: int
            検索数

        Returns
        -------
        dict
            取得したデータ辞書
        """
        if params['period'] is None:
            params['period'] = 'minute'

        if params['from'] is None:
            params['from'] = datetime.now() - timedelta(weeks=480)
        else:
            from_timestamp = int(params['from'])
            params['from'] = datetime.fromtimestamp(from_timestamp)

        if params['to'] is None:
            params['to'] = datetime.now() + timedelta(weeks=480)
        else:
            to_timestamp = int(params['to'])
            params['to'] = datetime.fromtimestamp(to_timestamp)

        filter_list = []
        filter_list.append({"timestamp": {'$gte': params['from']}})
        filter_list.append({"timestamp": {'$lte': params['to']}})

        db_col = self.db.get_collection(params['period'])

        item_list = [self.change_datetime(item) for item in db_col.find(
            sort=[('timestamp', -1)],
            projection={'_id': 0, },
            filter={'timestamp': {'$gte': params['from'], '$lt': params['to']}}
        ).limit(record_limit)]

        item_list.reverse()

        df = pd.DataFrame(item_list)
        result = df.to_dict(orient='list')

        return result

    def change_datetime(self, data):
        """datetime(UTC)をJSTの文字列に変換."""
        t_str = "%Y-%m-%d %H:%M:%S"
        data['timestamp'] = (data['timestamp'] + timedelta(hours=9)).strftime(
            t_str)

        return data
