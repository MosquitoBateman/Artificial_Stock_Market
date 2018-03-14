# -*- coding: utf-8 -*-
"""
@author: Jeffmxh
"""

import pandas as pd
import numpy as np
import ggplot as gp

from utils.Trader_basic import Order


class Dynamic_order:
    '''
    extension of Order, used in making deals
    '''
    def __init__(self, order):
        assert isinstance(order, Order)
        self.id = order.id
        self.price = order.price
        self.volume = order.volume

    @property
    def show(self):
        print('id : %d' % self.id)
        print('price : %d' % self.price)
        print('volume : %d' % self.volume)

class Market:
    '''
    A class to define a market stucture, initialize with a
    number of investors, have the ability to generate orders
    and deal with the orders from traders, returns a deal_price
    and volume for every trader and update their status
    The history of price and volume is also contained, as well
    as indices like MA and so on
    '''
    def __init__(self, Trader_class, num_investors, asset, stock_price):
        self.investors = [Trader_class(i, asset=asset, stock_price=stock_price) for i in range(num_investors)]
        self.price = [stock_price]
        self.vol = []
        self.MA_5 = []
        self.MA_10 = []
        self.MA_100 = []
        self.MA_500 = []

    def make_deals(self, orders):
        buy_list = [Dynamic_order(order) for order in orders if order.volume > 0]
        sell_list = [Dynamic_order(order) for order in orders if order.volume < 0]

        buy_list = sorted(buy_list, key=lambda x: (-x.price, x.id))
        sell_list = sorted(sell_list, key=lambda x: (x.price, x.id))
        deal_result = np.zeros(len(orders), int)
        price = 0
        if len(buy_list) == 0 or len(sell_list) == 0:
            return price, deal_result
        while buy_list[0].price - sell_list[0].price >= 0:
            if sell_list[0].volume + buy_list[0].volume <= 0:
                sell_list[0].volume += buy_list[0].volume
                deal_result[buy_list[0].id] += buy_list[0].volume
                deal_result[sell_list[0].id] -= buy_list[0].volume
                if sell_list[0].volume + buy_list[0].volume == 0:
                    price = (buy_list[0].price + sell_list[0].price) / 2
                else:
                    price = sell_list[0].price
                _ = buy_list.pop(0)
            else:
                buy_list[0].volume += sell_list[0].volume
                deal_result[buy_list[0].id] -= sell_list[0].volume
                deal_result[sell_list[0].id] += sell_list[0].volume
                price = buy_list[0].price
                _ = sell_list.pop(0)
            price = abs(price)
            if len(buy_list) == 0 or len(sell_list) == 0:
                break
        assert np.sum(deal_result) == 0
        self.update(price, deal_result)
        return price, deal_result

    def update(self, price, deal_result):
        self.price.append(price)
        self.vol.append(np.sum(deal_result))
        duration = len(self.price)
        self.MA_5.append(np.mean(self.price[-5:]) if duration > 5 else 0)
        self.MA_10.append(np.mean(self.price[-10:]) if duration > 10 else 0)
        self.MA_100.append(np.mean(self.price[-100:]) if duration > 100 else 0)
        self.MA_500.append(np.mean(self.price[-500:]) if duration > 500 else 0)

    def step(self):
        orders = []
        for investor in self.investors:
            investor.gen_order()
            orders.append(investor.order)

        price, deal_result = self.make_deals(orders)
        for i, investor in enumerate(self.investors):
            investor.update(price=price, vol=deal_result[i])

    @property
    def show_price(self):
        price_table = pd.DataFrame({'time_step':range(len(self.price)), 'price':self.price},
                                   columns=['time_step', 'price'])
        p = gp.ggplot(gp.aes(x='time_step', y='price'), data=price_table) + \
                    gp.geom_line() + \
                    gp.xlim(0, len(self.price)) + \
                    gp.ggtitle('Price trend')
        print(p)
