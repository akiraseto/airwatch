#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask."""

from flask import Flask, jsonify

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
    """ダイキンデータAPI."""
    # todo:Paramの取得
    res = daikin.get_data()

    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

# todo:flaskでダイキンデータ取得
