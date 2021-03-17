#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダイキンセンサーモデル."""

import os
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

    def get_data(self, params):
        """
        データを取得.

        Parameters
        ----------
        params : dict
            検索パラメーター

        Returns
        -------
        dict
            取得したデータ辞書
        """
        if params['period'] is None or params['period'] == '':
            params['period'] = 'minute'
        if params['limit'] is None or params['limit'] == '':
            if params['period'] == 'minute':
                params['limit'] = round(60 * 24 / int(os.environ[
                                                           'BASIC_MINUTE']))
            elif params['period'] == 'hour':
                params['limit'] = 168
            else:
                params['limit'] = 120
        else:
            params['limit'] = int(params['limit'])

        if params['from'] is None or params['from'] == '':
            params['from'] = datetime.now() - timedelta(weeks=480)
        else:
            from_timestamp = int(params['from'])
            params['from'] = datetime.fromtimestamp(from_timestamp)

        if params['to'] is None or params['to'] == '':
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
        ).limit(params['limit'])]

        item_list.reverse()

        df = pd.DataFrame(item_list)
        result = df.to_dict('list')

        return result

    def change_datetime(self, data):
        """datetime(UTC)をJSTの文字列に変換."""
        t_str = "%Y-%m-%d %H:%M:%S"
        data['timestamp'] = (data['timestamp'] + timedelta(hours=9)).strftime(
            t_str)

        return data
