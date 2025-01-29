import yfinance as yf

df = yf.download('2317.TW', start='2020-01-01', end='2023-12-31')
df.columns = df.columns.get_level_values(0)
print(df.head())