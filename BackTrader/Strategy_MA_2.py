#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:  kerwin.cn@gmail.com
# Created Time:2017-09-20 20:49:18
# Last Change:  2017-11-10 20:52:02
# File Name: sample1.py

import backtrader as bt
import CerebroBase
import StrategyBase


# Create a Stratey
# 这个是均线系统，我大选系统如下：
# 当五日均线突破10日均线的时候，10%仓位
# 当MACD出现突破的时候，10%仓位。
class Strategy_MA(StrategyBase.StrategyBase):

    params = (('ma1', 5), ('ma2', 10), ('ma3', 20))

    def __init__(self):
        # 添加多条均线
        self.sma1 = bt.talib.SMA(self.data, timeperiod=self.params.ma1)
        self.sma2 = bt.talib.SMA(self.data, timeperiod=self.params.ma2)
        self.sma3 = bt.talib.SMA(self.data, timeperiod=self.params.ma3)
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        # 先求还有多少钱吧, cash是get_cash, 如果是要资产是get_value()
        cash = self.broker.get_cash()
        # value = self.broker.get_value()
        # 获得开盘价格，我是根据开盘价格来交易的。
        open_price = self.data_open[0]

        size1 = int(cash / open_price * 0.15)
        # size2 = int(value/open_price*0.25)
        # 当5日均线上穿10日均线的时候，买入
        if(self.sma1[0] > self.sma2[0] and
           self.sma1[-1] < self.sma2[-1]):
            # 首先取消原先的单子吧
            #  already_size = self.position.size
            # if(already_size < 0):
            # self.close()
            # already_size = 0
            # self.buy_bracket(size=size1, price=open_price, stopprice=open_price-60)
            self.buy(size=size1)

        if(self.sma1[0] < self.sma2[0] and
           self.sma1[-1] > self.sma2[-1]):
            # 首先取消原先的单子吧
            # already_size = self.position.size
            # if(already_size > 0):
            # self.close()
            # already_size = 0
            # self.sell_bracket(size=size1, price=open_price, stopprice=open_price+60)
            self.sell(size=size1)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = CerebroBase.CerebroAGUSDO()
    # Add a strategy
    cerebro.addstrategy(Strategy_MA)
    # Set our desired cash start
    cerebro.set_cash(100000.0)

    cerebro.run()