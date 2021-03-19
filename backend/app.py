#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask."""

from flask import Flask, jsonify, request

from models.daikin import Daikin
from models.gpio import Gpio

app = Flask(__name__)
daikin = Daikin()
gpio = Gpio()


@app.route('/')
def hello():
    """デフォルトページ."""
    name = "Let's connect with RESTFUL API"
    return name


@app.route('/v1/daikin')
def get_daikin_data():
    """ダイキンデータAPI.

    query:dict
        from: int
            timestamp
        to: int
            timestamp
        period: string
            minute, hour, day, week
    """
    params = {
        'from': request.args.get('from'),
        'to': request.args.get('to'),
        'period': request.args.get('period'),
        'limit': request.args.get('limit'),
    }

    res = daikin.get_data(params)

    return jsonify(res)


@app.route('/v1/gpio')
def get_gpio_data():
    """GPIOデータAPI.

    query:dict
        from: int
            timestamp
        to: int
            timestamp
        period: string
            minute, hour, day, week
    """
    params = {
        'from': request.args.get('from'),
        'to': request.args.get('to'),
        'period': request.args.get('period'),
        'limit': request.args.get('limit'),
    }

    res = {
        'bmp': gpio.get_bmp_data(params),
        'dht': gpio.get_dht_data(params),
    }

    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
