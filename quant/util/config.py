#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/10/31 17:28
@annotation = ''
"""
import collections
import os

import pandas as pd
import yaml

from quant.const import FREQUENCY, RUN_TYPE, ACCOUNT_TYPE
from quant.modle.instrument import Instrument
from quant.util import AttrDict

default_mod_config_path = os.path.join(os.path.dirname(__file__), '..', 'mod_config.yml')
default_instrument_config_path = os.path.join(os.path.dirname(__file__), '..', 'instrument.yml')


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def dump_yaml(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        return yaml.safe_dump(data, f)


def load_mod_conf():
    conf = load_yaml(default_mod_config_path)
    return conf


def load_instrument_conf():
    conf = load_yaml(default_instrument_config_path)
    return conf


def deep_update(from_dict, to_dict):
    for key, value in from_dict.items():
        if key in to_dict.keys() \
                and isinstance(to_dict[key], collections.Mapping) \
                and isinstance(value, collections.Mapping):
            deep_update(value, to_dict[key])
        else:
            to_dict[key] = value


def get_all_instrument():
    instrument_info = load_instrument_conf()
    instruments = load_instrument_conf()
    for exchange, infos in instrument_info.items():
        for info in infos:
            instrument = Instrument(exchange, **info)
            instruments[instrument.symbol] = instrument
    return instruments


# TODO:持久化
def parse_config(config):
    def parse_date(config_date):
        # dt = datetime.datetime.strptime(config_date, "%Y-%m-%d")
        # return dt.replace(microsecond=0)
        return pd.Timestamp(config_date)

    def parse_account(account):
        a = {account_type.name: float(start_cash) for account_type, start_cash in account.items()
             if start_cash is not None and account_type in ACCOUNT_TYPE.__members__.values()}
        assert len(a) != 0
        return a

    deep_update(load_mod_conf(), config)
    config = AttrDict(config)
    base_config = config.base

    base_config.start_date = parse_date(base_config.start_date)
    base_config.end_date = parse_date(base_config.end_date)
    base_config.account = parse_account(base_config.account)
    assert base_config.start_date < base_config.end_date
    assert base_config.run_type in RUN_TYPE.__members__.values()
    assert base_config.frequency in FREQUENCY.ALL
    assert base_config.symbol in get_all_instrument()
    config.base = base_config

    return config
