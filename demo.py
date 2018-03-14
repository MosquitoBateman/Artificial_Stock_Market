# -*- coding: utf-8 -*-
"""
@author: Jeffmxh
"""


from utils.Trader_basic import Basic_Trader
from utils.Market import Market
from Advanced_Trader import Advanced_Trader

def main():
    market = Market(Advanced_Trader, 30, asset=1000, stock_price=10.0)
    for _ in range(30):
        market.step()

    total_asset = 0
    for investor in market.investors:
        investor.show
        total_asset += investor.asset

    print('Total asset : ', total_asset)

if __name__ == '__main__':
    main()
