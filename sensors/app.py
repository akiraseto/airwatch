#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""エンドポイントファイル."""

import datetime
import logging
import os

import time

from models.daikin import Daikin

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    daikin = Daikin()

    minutes_time = int(os.environ['BASIC_MINUTE'])

    latest_record = {}
    periods = ['minute', 'hour', 'day', 'week']
    delta_list = {}
    delta_list['minute'] = datetime.timedelta(minutes=1)
    delta_list['hour'] = datetime.timedelta(hours=1)
    delta_list['day'] = datetime.timedelta(days=1)
    delta_list['week'] = datetime.timedelta(weeks=1)

    # 初期化:DBにデータ無ければ即インサート
    data = daikin.get_sensor()
    for period in periods:
        latest_record[period] = daikin.find_latest(period)
        if latest_record[period] is None:
            daikin.insert_data(period, data)
            latest_record[period] = data

    while True:
        now = datetime.datetime.now()
        data = daikin.get_sensor()
        logging.info('daikin:{}'.format(data))

        for period in periods:
            if now >= latest_record[period]['timestamp'] + delta_list[period]:
                daikin.insert_data(period, data)
                latest_record[period] = data

        time.sleep(minutes_time * 60)
