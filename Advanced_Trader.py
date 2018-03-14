# -*- coding: utf-8 -*-

"""
@author: Jeffmxh
"""

import math
import random
import numpy as np

from collections import namedtuple

from utils.Trader_basic import Basic_Trader, Order

class Advanced_Trader(Basic_Trader):
    '''
    An example to extend the Basic_Trader class, this kind
    of traders have the chance of 60% to trade, the price
    is given by previous stock price with a jitter, the sign
    of jitter indicates buying or selling, stock hold must be
    positive
    '''
    def gen_order(self):
        '''
        Redefine the function in Basic_Trader for generating order
        '''
        TRADE_PROB = 0.6
        trade_bool = random.random()
        if trade_bool < TRADE_PROB:
            eps = np.random.randn()
            price = np.max([self.stock_price + eps, 1])
            if eps > 0:
                vol_max = math.floor(self.cash / price)
                volume = np.random.randint(0, vol_max) if vol_max>0 else 0
            else:
                volume = np.random.randint(-self.stock, 0) if self.stock>0 else 0
        else:
            price = 0
            volume = 0
        self.order = Order(id=self.id,
                           price=price,
                           volume=volume)
