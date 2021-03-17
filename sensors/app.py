#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""エンドポイントファイル."""

import datetime
import logging
import os

import time

from models.daikin import Daikin
from models.gpio import Gpio

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    daikin = Daikin()
    gpio = Gpio()

    minutes_time = int(os.environ['BASIC_MINUTE'])

    latest_record = {}
    latest_record_gpio = {}
    periods = ['minute', 'hour', 'day', 'week']
    delta_list = {}
    delta_list['minute'] = datetime.timedelta(minutes=1)
    delta_list['hour'] = datetime.timedelta(hours=1)
    delta_list['day'] = datetime.timedelta(days=1)
    delta_list['week'] = datetime.timedelta(weeks=1)

    # 初期化:DBにデータ無ければ即インサート
    data_daikin = daikin.get_sensor()
    data_gpio = gpio.get_sensor()
    for period in periods:
        latest_record[period] = daikin.find_latest(period)
        if latest_record[period] is None:
            daikin.insert_data(period, data_daikin)
            latest_record[period] = data_daikin

        latest_record_gpio[period] = gpio.find_latest(period)
        if latest_record_gpio[period] is None:
            gpio.insert_data(period, data_gpio)
            latest_record[period] = data_gpio

    while True:
        now = datetime.datetime.now()
        data_daikin = daikin.get_sensor()
        data_gpio = gpio.get_sensor()
        logging.info('daikin:{}'.format(data_daikin))
        logging.info('gpio:{}'.format(data_gpio))

        for period in periods:
            if now >= latest_record[period]['timestamp'] + delta_list[period]:
                daikin.insert_data(period, data_daikin)
                latest_record[period] = data_daikin

            if now >= latest_record_gpio[period]['timestamp'] \
                    + delta_list[period]:
                gpio.insert_data(period, data_gpio)
                latest_record_gpio[period] = data_gpio

        time.sleep(minutes_time * 60)
