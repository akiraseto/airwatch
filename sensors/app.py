#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""エンドポイントファイル."""

import logging
import os
import time

from models.daikin import Daikin

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    daikin = Daikin()

    inter_time = int(os.environ['INTERVAL'])

    while True:
        data = daikin.get_sensor()
        daikin.insert_data(data)

        logging.info('daikin:{}'.format(data))
        time.sleep(inter_time)
