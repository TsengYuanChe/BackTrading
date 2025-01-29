import backtrader as bt


"""-------------------簡單移動平均線 (SMA)-------------------"""
def SMA10(data):
    """ 計算 10 日簡單移動平均線 (SMA) """
    return bt.indicators.SimpleMovingAverage(data.close, period=10)

def SMA20(data):
    """ 計算 20 日簡單移動平均線 (SMA) """
    return bt.indicators.SimpleMovingAverage(data.close, period=20)

def SMA30(data):
    """ 計算 30 日簡單移動平均線 (SMA) """
    return bt.indicators.SimpleMovingAverage(data.close, period=30)

def SMA50(data):
    """ 計算 50 日簡單移動平均線 (SMA) """
    return bt.indicators.SimpleMovingAverage(data.close, period=50)

def SMA200(data):
    """ 計算 200 日簡單移動平均線 (SMA) """
    return bt.indicators.SimpleMovingAverage(data.close, period=200)