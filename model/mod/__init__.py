#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2017/5/24 16:08
@annotation = ''
"""
import copy

from model import AttrDict


def import_mod(mod_name):
    try:
        from importlib import import_module
        return import_module(mod_name)
    except Exception as e:
        pass


class ModHandler(object):
    def __init__(self, env):
        self._env = env
        self._mod_list = []
        self._mod_dict = {}

    def _set_up(self):
        for mod_name in SYSTEM_MOD_LIST:
            lib_name = "model.mod.mod_" + mod_name
            mod_module = import_mod(lib_name)
            mod_config = AttrDict(copy.deepcopy(getattr(mod_module, "__config__", {})))
            self._mod_list.append((mod_name, mod_config))
            mod = mod_module.load_mod()
            self._mod_dict[mod_name] = mod
        self._mod_list = sorted(self._mod_list, key=lambda item: getattr(item[1], "priority", 100))

    def start(self):
        self._set_up()
        for mod_name, mod_config in self._mod_list:
            self._mod_dict[mod_name].start(self._env, mod_config)

    def stop(self, *args, **kwargs):
        result = {}
        for mod_name, _ in reversed(self._mod_list):
            ret = self._mod_dict[mod_name].stop(*args, **kwargs)
            if ret is not None:
                result[mod_name] = ret
        return result


SYSTEM_MOD_LIST = [
    "sys_analyser",
    "sys_progress",
    "sys_settlement",
    # "sys_bot",
    # "sys_signal",
]
