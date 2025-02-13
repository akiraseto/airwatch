#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""データベース設定."""

import os
from datetime import datetime, timedelta

import pandas as pd
from pymongo import MongoClient


class MongoDB:
    """センサーDB."""

    def __init__(self):
        """イニシャライザ."""
        db_host = os.environ['DB_HOST']
        db_port = 27017

        self.client = MongoClient(db_host, db_port)
        self.db = None

    def get_data(self, params):
        """
        DBデータを取得.

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
        if params['limit'] is None or params['limit'] == '' or params[
                'limit'] == 'NaN':
            if params['period'] == 'minute':
                # 1日分
                params['limit'] = round(60 * 24 / int(os.environ[
                                                          'BASIC_MINUTE']))
            elif params['period'] == 'hour':
                # 4年分
                params['limit'] = 4 * 365 * 24
            else:
                # 10年分
                params['limit'] = 10 * 12 * 4
        else:
            params['limit'] = int(params['limit'])

        if params['from'] is None or params['from'] == '':
            params['from'] = datetime.now() - timedelta(weeks=480)
        elif isinstance(params['from'], datetime):
            pass
        else:
            from_timestamp = int(params['from'])
            params['from'] = datetime.fromtimestamp(from_timestamp)

        if params['to'] is None or params['to'] == '':
            params['to'] = datetime.now() + timedelta(weeks=480)
        elif isinstance(params['to'], datetime):
            pass
        else:
            to_timestamp = int(params['to'])
            params['to'] = datetime.fromtimestamp(to_timestamp)

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

    @staticmethod
    def change_datetime(data):
        """datetime(UTC)をJSTの文字列に変換."""
        t_str = "%Y-%m-%d %H:%M:%S"
        data['timestamp'] = (data['timestamp'] + timedelta(hours=9)).strftime(
            t_str)

        return data
