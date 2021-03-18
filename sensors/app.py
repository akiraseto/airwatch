#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""エンドポイントファイル."""

import datetime
import logging
import os
import time
from collections import defaultdict

from models.bmp import Bmp
from models.daikin import Daikin
from models.dht import Dht

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    daikin = Daikin()
    bmp = Bmp()
    dht = Dht()

    minutes_time = int(os.environ['BASIC_MINUTE'])

    latest_data = defaultdict(dict)
    periods = ['minute', 'hour', 'day', 'week']
    delta_list = {}
    delta_list['minute'] = datetime.timedelta(minutes=1)
    delta_list['hour'] = datetime.timedelta(hours=1)
    delta_list['day'] = datetime.timedelta(days=1)
    delta_list['week'] = datetime.timedelta(weeks=1)

    # 最新DBデータ取得
    for period in periods:
        latest_data['daikin'][period] = daikin.find_latest(period)
        latest_data['bmp'][period] = bmp.find_latest(period)
        latest_data['dht'][period] = dht.find_latest(period)

    while True:
        now = datetime.datetime.now()
        data_daikin = daikin.get_sensor()
        data_bmp = bmp.get_sensor()
        data_dht = dht.get_sensor()
        logging.info('daikin:{}'.format(data_daikin))
        logging.info('bmp:{}'.format(data_bmp))
        logging.info('dht:{}'.format(data_dht))

        for period in periods:
            if latest_data['daikin'][period] is None or \
                    now >= latest_data['daikin'][period]['timestamp'] \
                    + delta_list[period]:
                if data_daikin is not None:
                    daikin.insert_data(period, data_daikin)
                    latest_data['daikin'][period] = data_daikin

            if latest_data['bmp'][period] is None or \
                    now >= latest_data['bmp'][period]['timestamp'] \
                    + delta_list[period]:
                if data_bmp is not None:
                    bmp.insert_data(period, data_bmp)
                    latest_data['bmp'][period] = data_bmp

            if latest_data['dht'][period] is None or \
                    now >= latest_data['dht'][period]['timestamp'] \
                    + delta_list[period]:
                if data_dht is not None:
                    dht.insert_data(period, data_dht)
                    latest_data['dht'][period] = data_dht

        time.sleep(minutes_time * 60)
