# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from quant import AbstractValidator, SIDE, ACCOUNT_TYPE


class CashValidator(AbstractValidator):
    def __init__(self, env):
        self._env = env

    def _crypto_validator(self, account, order):
        if order.side == SIDE.SELL:
            return True
        # 检查可用资金是否充足
        cost_money = order.price * order.amount
        if cost_money <= account.cash:
            return True

        order.reject(
            "Order Rejected: not enough money to buy {symbol}, needs {cost_money:.2f}, "
            "cash {cash:.2f}".format(
                symbol=order.symbol,
                cost_money=cost_money,
                cash=account.cash,
            )
        )
        return False

    def can_submit_order(self, account, order):
        if account.type == ACCOUNT_TYPE.CRYPTO.name:
            return self._crypto_validator(account, order)
        else:
            raise NotImplementedError

    def can_cancel_order(self, account, order):
        return True
