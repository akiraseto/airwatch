#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダイキンセンサーモデル."""

from db import MongoDB


class Daikin(MongoDB):
    """ダイキンデータDB."""

    def __init__(self):
        """イニシャライザ."""
        super().__init__()

        col_name = 'daikin'
        self.db_col = self.db.get_collection(col_name)

    def get_data(self, params=None, record_limit=100):
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
        list
            取得したデータリスト
        """

        if params is None:
            params = {}
        if 'from' not in params:
            params['from'] = ['2000-01-01 00:00']
        if 'to' not in params:
            params['to'] = ['2100-12-31 23:59']

        filter_list = []
        filter_list.append({"timestamp": {'$gte': params['from']}})
        filter_list.append({"timestamp": {'$lte': params['to']}})

        item_list = [self.delete_object_id(item) for item in
                     self.db_col.find(sort=[('timestamp', -1)]).limit(
                         record_limit)]

        return item_list

    def delete_object_id(self, dic):
        dic.pop('_id')
        return dic
    #
    # def get_data(self, params, record_limit):
    #     """
    #     データを取得.
    #
    #     Parameters
    #     ----------
    #     params : dict
    #         検索パラメーター
    #     record_limit: int
    #         検索数
    #
    #     Returns
    #     -------
    #     dict
    #         データベースから取得されたデータ辞書
    #     """
    #     res_dict = {}
    #
    #
    #     filter_list = []
    #     filter_list.append({"timestamp": {'$gte': params['from']}})
    #     filter_list.append({"timestamp": {'$lte': params['to']}})
    #
    #     recs = self.db_col.find(projection=None, sort=[('timestamp', -1)],
    #                             filter={'$and': filter_list}).limit(
    #         record_limit)
    #
    #     return res_dict
