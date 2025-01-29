import backtrader as bt

class SmaCross(bt.Strategy):
    params = (
        ('sma_short', 10),  # 短期移動平均線
        ('sma_long', 30),   # 長期移動平均線
    )

    def __init__(self):
        # 定義短期與長期移動平均線
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_short)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_long)

        # 初始化交易記錄變數
        self.trade_records = []  # 只記錄當前策略的交易記錄

    def next(self):
        # 買入條件：短期均線向上穿越長期均線
        allocation = 450000  # 定義每次交易的資金

    # 確保有足夠的資金進行交易
        if self.broker.getcash() > allocation:
            # 買入條件：短期均線向上穿越長期均線
            if self.sma_short > self.sma_long and not self.position:
                size = allocation // self.data.close[0]  # 根據當前收盤價計算股數
                self.buy(size=1)
            # 賣出條件：短期均線向下穿越長期均線
            elif self.sma_short < self.sma_long and self.position:
                self.sell(size=1)  # 全部賣出持倉

    def notify_order(self, order):
        if order.status in [order.Completed]:  # 確認訂單已完成
            action = 'Buy' if order.isbuy() else 'Sell'
            self.trade_records.append({
                'datetime': self.data.datetime.datetime(0),  # 獲取交易時間
                'action': action,
                'price': order.executed.price,
                'size': order.executed.size,
                'value': order.executed.value,
                'commission': order.executed.comm
            })
        