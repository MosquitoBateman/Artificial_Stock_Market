# -*- coding: utf-8 -*-
"""
@author: Jeffmxh
"""

import math
import random

from collections import namedtuple
import pandas as pd
import numpy as np
import ggplot as gp


'''
struct to storage order price and volume to trade

Usage:
a = Order(price=1, volume=1)
'''

Order = namedtuple('order', 'id price volume')


class Basic_Trader:
    '''
    A primary class to define an investor, including actions
    like gennerate an order, and update it's own status with
    the trading result
    '''
    def __init__(self, id, asset, stock_price, *kw, **args):
        self.id = id
        self.asset = asset # 总资产
        self.stock_price = stock_price
        self.cash, self.stock = self.random_init(asset, stock_price)
        self.cash_history = [self.cash]
        self.asset_history = [self.asset]
        self.stock_history = [self.stock]
        self.trade_history = [] # 交易记录
        self.order = Order(id=self.id,
                           price=0,
                           volume=0)

    def random_init(self, asset, stock_price):
        stock_max = math.floor(asset/stock_price)
        stock_num = random.randint(0, stock_max)
        cash = asset - stock_num * stock_price
        return cash, stock_num

    def gen_order(self):
        self.order = Order(id=self.id,
                           price=np.random.randint(1, 20),
                           volume=np.random.randint(-5, 5))

    def update(self, price, vol):
        self.cash -= price * vol
        self.cash_history.append(self.cash)
        self.stock += vol
        self.stock_history.append(self.stock)
        self.trade_history.append((price, vol))
        self.stock_price = price
        self.asset = self.cash + self.stock * self.stock_price
        self.asset_history.append(self.asset)

    @property
    def show(self):
        print('id : %d, cash : %d, stock : %d, stock_price : %d, asset : %d' %
              (self.id, self.cash, self.stock, self.stock_price, self.asset))

    @property
    def show_detail(self):
        print('id : ', self.id)
        print('cash : ', self.cash)
        print('cash_history : ', self.cash_history)
        print('stock : ', self.stock)
        print('stock_history : ', self.stock_history)
        print('asset : ', self.asset)
        print('asset_history : ', self.asset_history)
        print('stock_price : ', self.stock_price)

    @property
    def show_asset(self):
        asset_table = pd.DataFrame({'time_step':range(len(self.asset_history)), 'asset':self.asset_history},
                           columns=['time_step', 'asset'])
        p = gp.ggplot(gp.aes(x='time_step', y='asset'), data = asset_table) + \
                   gp.geom_line() + \
                   gp.xlim(0, len(self.asset_history)) + \
                   gp.ggtitle('Asset trend')
        print(p)
