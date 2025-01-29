import pandas as pd
from trader import run_backtest
from strategy import SmaCross
import os

method = SmaCross
method_name = method.__name__
output_dir = f"./results/{method_name}"  # 存放結果的資料夾
os.makedirs(output_dir, exist_ok=True)

# 讀取股票清單
stock_list_path = "stock_list.csv"
stock_list = pd.read_csv(stock_list_path)

# 只保留必要的欄位
stock_list = stock_list[["代號", "股票名稱"]]

# 將代號轉換為帶 ".TW" 的格式（假設回測需要這種格式）
stock_list["代號"] = stock_list["代號"].apply(lambda x: f"{x}.TW")

# 定義回測時間
start_date = '2022-01-01'
end_date = '2024-12-31'

# 保存結果
results = []

# 遍歷股票清單，進行回測
for _, row in stock_list.iterrows():
    stock_code = row["代號"]
    stock_name = row["股票名稱"]
    print(f"正在回測股票: {stock_code} ({stock_name})")

    try:
        # 執行回測
        result = run_backtest(stock_code, start_date, end_date, method)
        # 添加代號和名稱到結果
        if result and "win_rate" in result:
            # 添加代號和名稱到結果
            result["代號"] = stock_code
            result["股票名稱"] = stock_name
            results.append(result)
            print(f"{stock_code} ({stock_name}) 的獲利成功率: {result['win_rate']:.2f}%")
        else:
            print(f"{stock_code} ({stock_name}) 的回測結果無效，跳過該股票。")
    except Exception as e:
        print(f"回測失敗: {stock_code} ({stock_name})，錯誤: {e}")

if results:
    df = pd.DataFrame(results)

    # 展平前三大獲利與虧損比例
    df['top_profit_ratios'] = df['top_profit_ratios'].apply(lambda x: ', '.join([f"{y:.2f}%" for y in x]))
    df['top_loss_ratios'] = df['top_loss_ratios'].apply(lambda x: ', '.join([f"{y:.2f}%" for y in x]))

    # 計算平均獲利成功率
    avg_win_rate = df['win_rate'].mean()

    # 動態生成 CSV 文件名
    file_name = f"{method_name} has average winrate {avg_win_rate:.2f}% from {start_date} to {end_date}.csv"
    file_path = os.path.join(output_dir, file_name)
    df.to_csv(file_path, index=False)
    print(f"所有股票的回測結果已保存至 '{file_path}'")
else:
    print("沒有有效的回測結果，未生成 CSV 文件。")