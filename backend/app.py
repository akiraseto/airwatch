#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask."""

from flask import Flask, jsonify, request

from models.daikin import Daikin

app = Flask(__name__)
daikin = Daikin()


@app.route('/')
def hello():
    """デフォルトページ."""
    name = "Let's connect with RESTFUL API"
    return name


@app.route('/api/v1/daikin')
def get_daikin_data():
    """ダイキンデータAPI.

    query:dict
        from: int
            timestamp
        to: int
            timestamp
        period: string
            5m, hour, day, week
    """
    params = {
        'from': request.args.get('from'),
        'to': request.args.get('to'),
        'period': request.args.get('period'),
    }

    res = daikin.get_data(params)

    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
