#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""エンドポイントファイル."""

import datetime
import logging
import os
from collections import defaultdict

import time

from models.bmp import Bmp
from models.daikin import Daikin
from models.dht import Dht
from models.sgp import Sgp

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    sensors = [
        Daikin(),
        Bmp(),
        Dht(),
        Sgp()
    ]

    periods = ['minute', 'hour', 'day', 'week']
    delta_list = {}
    delta_list['minute'] = datetime.timedelta(minutes=1)
    delta_list['hour'] = datetime.timedelta(hours=1)
    delta_list['day'] = datetime.timedelta(days=1)
    delta_list['week'] = datetime.timedelta(weeks=1)

    # 最新DBデータ取得
    latest_data = defaultdict(dict)
    for period in periods:
        for sensor in sensors:
            name = sensor.__str__()
            latest_data[name][period] = sensor.find_latest(period)

    minutes_time = int(os.environ['BASIC_MINUTE'])
    while True:
        now = datetime.datetime.now()
        data_sensors = {}
        for sensor in sensors:
            name = sensor.__str__()
            data = sensor.get_sensor()
            data_sensors[name] = data
            logging.info('{}:{}'.format(name, data))

        for period in periods:
            for sensor in sensors:
                name = sensor.__str__()
                if latest_data[name][period] is None or \
                        now >= latest_data[name][period]['timestamp'] \
                        + delta_list[period]:
                    if data_sensors[name] is not None:
                        sensor.insert_data(period, data_sensors[name])
                        latest_data[name][period] = data_sensors[name]

        time.sleep(minutes_time * 60)
