#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/31 15:24
@annotation = ''
"""
from quant import Instrument

crypto_instrument = {
    "okcn": [
        {
            "pair": "btc_cny",
            "fee": 0.2,
            "min_amount": 0.01,
        },
        {
            "pair": "ltc_cny",
            "fee": 0.2,
            "min_amount": 0.1,
        },
    ],
}


def get_all_crypto():
    instruments = {}
    for exchange, infos in crypto_instrument.items():
        for info in infos:
            instrument = Instrument(exchange, **info)
            instruments[instrument.symbol] = instrument
    return instruments
