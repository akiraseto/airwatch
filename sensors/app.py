#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""エンドポイントファイル."""

import datetime
import logging
import os
import time

from models.bmp import Bmp
from models.dht import Dht
from models.daikin import Daikin

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    daikin = Daikin()
    bmp = Bmp()
    dht = Dht()

    minutes_time = int(os.environ['BASIC_MINUTE'])

    latest_daikin_data = {}
    latest_bmp_data = {}
    latest_dht_data = {}
    periods = ['minute', 'hour', 'day', 'week']
    delta_list = {}
    delta_list['minute'] = datetime.timedelta(minutes=1)
    delta_list['hour'] = datetime.timedelta(hours=1)
    delta_list['day'] = datetime.timedelta(days=1)
    delta_list['week'] = datetime.timedelta(weeks=1)

    # 初期化:DBにデータ無ければ即インサート
    data_daikin = daikin.get_sensor()
    data_bmp = bmp.get_sensor()
    data_dht = dht.get_sensor()
    for period in periods:
        latest_daikin_data[period] = daikin.find_latest(period)
        if latest_daikin_data[period] is None:
            daikin.insert_data(period, data_daikin)
            latest_daikin_data[period] = data_daikin

        latest_bmp_data[period] = bmp.find_latest(period)
        if latest_bmp_data[period] is None:
            bmp.insert_data(period, data_bmp)
            latest_bmp_data[period] = data_bmp

        latest_dht_data[period] = dht.find_latest(period)
        if latest_dht_data[period] is None:
            dht.insert_data(period, data_dht)
            latest_dht_data[period] = data_dht

    while True:
        now = datetime.datetime.now()
        data_daikin = daikin.get_sensor()
        data_bmp = bmp.get_sensor()
        data_dht = dht.get_sensor()
        logging.info('daikin:{}'.format(data_daikin))
        logging.info('bmp:{}'.format(data_bmp))
        logging.info('dht:{}'.format(data_dht))

        for period in periods:
            if now >= latest_daikin_data[period]['timestamp'] \
                    + delta_list[period]:
                daikin.insert_data(period, data_daikin)
                latest_daikin_data[period] = data_daikin

            if now >= latest_bmp_data[period]['timestamp'] \
                    + delta_list[period]:
                bmp.insert_data(period, data_bmp)
                latest_bmp_data[period] = data_bmp

            if now >= latest_dht_data[period]['timestamp'] \
                    + delta_list[period]:
                dht.insert_data(period, data_dht)
                latest_dht_data[period] = data_dht

        time.sleep(minutes_time * 60)
