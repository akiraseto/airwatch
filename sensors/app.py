#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""エンドポイントファイル."""

import datetime
import logging
import os
import time

from models.bmp import Bmp
from models.daikin import Daikin

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    daikin = Daikin()
    bmp = Bmp()

    minutes_time = int(os.environ['BASIC_MINUTE'])

    latest_daikin_data = {}
    latest_bmp_data = {}
    periods = ['minute', 'hour', 'day', 'week']
    delta_list = {}
    delta_list['minute'] = datetime.timedelta(minutes=1)
    delta_list['hour'] = datetime.timedelta(hours=1)
    delta_list['day'] = datetime.timedelta(days=1)
    delta_list['week'] = datetime.timedelta(weeks=1)

    # 初期化:DBにデータ無ければ即インサート
    data_daikin = daikin.get_sensor()
    data_bmp = bmp.get_sensor()
    for period in periods:
        latest_daikin_data[period] = daikin.find_latest(period)
        if latest_daikin_data[period] is None:
            daikin.insert_data(period, data_daikin)
            latest_daikin_data[period] = data_daikin

        latest_bmp_data[period] = bmp.find_latest(period)
        if latest_bmp_data[period] is None:
            bmp.insert_data(period, data_bmp)
            latest_bmp_data[period] = data_bmp

    while True:
        now = datetime.datetime.now()
        data_daikin = daikin.get_sensor()
        data_bmp = bmp.get_sensor()
        logging.info('daikin:{}'.format(data_daikin))
        logging.info('bmp:{}'.format(data_bmp))

        for period in periods:
            if now >= latest_daikin_data[period]['timestamp'] \
                    + delta_list[period]:
                daikin.insert_data(period, data_daikin)
                latest_daikin_data[period] = data_daikin

            if now >= latest_bmp_data[period]['timestamp'] \
                    + delta_list[period]:
                bmp.insert_data(period, data_bmp)
                latest_bmp_data[period] = data_bmp

        time.sleep(minutes_time * 60)
