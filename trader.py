import backtrader as bt
import yfinance as yf
from strategy import SmaCross  # 引入策略
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# 設置 Matplotlib 的非顯示後端
matplotlib.use('Agg')

def run_backtest(stock, start_date, end_date, method):
    # 建立回測引擎
    cerebro = bt.Cerebro()

    # 添加策略
    cerebro.addstrategy(method)

    # 載入股票歷史數據
    df = yf.download(stock, start=start_date, end=end_date)

    # 展平多重索引並重命名欄位
    df.columns = df.columns.get_level_values(0)
    df.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        },
        inplace=True
    )

    # 檢查和處理 NaN 或 Inf 值
    df.replace([float('inf'), float('-inf')], None, inplace=True)
    df.dropna(inplace=True)

    # 確認是否有 volume 欄位
    if 'volume' not in df.columns or df['volume'].isnull().all():
        df['volume'] = 0

    # 設置索引為 UTC 時區
    df.index = df.index.tz_localize('UTC')

    # 將格式化的數據載入到 Backtrader
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # 設定初始資金
    InitialValue = 1000000
    cerebro.broker.setcash(InitialValue)

    # 設定交易手續費
    cerebro.broker.setcommission(commission=0.001425)

    # 執行回測
    initial_cash = cerebro.broker.getvalue()
    strategies = cerebro.run()
    strategy = strategies[0]
    final_cash = cerebro.broker.getvalue()
    return_rate = (final_cash - initial_cash) / initial_cash * 100

    # 保存交易記錄
    trade_df = pd.DataFrame(strategy.trade_records)

    # 統計交易數據
    total_trades = len(trade_df) // 2  # 每次交易包括買入和賣出
    profits = []
    losses = []
    profit_ratios = []
    loss_ratios = []

    for i in range(0, len(trade_df), 2):
        # 確保有完整的買入和賣出記錄
        if i + 1 < len(trade_df):
            buy_trade = trade_df.iloc[i]
            sell_trade = trade_df.iloc[i + 1]
            pnl = (sell_trade['price'] - buy_trade['price']) * buy_trade['size']
            ratio = (pnl / (buy_trade['price'] * buy_trade['size'])) * 100  # 獲利/虧損比例
            if pnl > 0:
                profits.append(pnl)
                profit_ratios.append(ratio)
            else:
                losses.append(pnl)
                loss_ratios.append(ratio)

    profit_count = len(profits)  # 獲利次數
    loss_count = len(losses)    # 虧損次數
    win_rate = (profit_count / total_trades) * 100 if total_trades > 0 else 0

    # 獲取前三大獲利比例和前三大虧損比例
    top_profit_ratios = sorted(profit_ratios, reverse=True)[:3]
    top_loss_ratios = sorted(loss_ratios)[:3]  # 由於是負數，直接排序即可

    return {
        "stock": stock,
        "total_trades": total_trades,
        "profit_count": profit_count,
        "loss_count": loss_count,
        "win_rate": win_rate,
        "top_profit_ratios": top_profit_ratios,
        "top_loss_ratios": top_loss_ratios,
    }