import pandas as pd
import numpy as np

dates = pd.date_range("2024-01-01", periods=200, freq="5min")

price = 0.85 + np.cumsum(np.random.randn(200) * 0.00005)

# делаем флэт
price[:100] = 0.85 + np.random.randn(100) * 0.00005

# РЕЗКИЙ ПРОБОЙ
price[100:105] += 0.003

df = pd.DataFrame({
    "time": dates,
    "open": price,
    "high": price + 0.0003,
    "low": price - 0.0003,
    "close": price,
    "volume": 100
})

df.to_csv("data/data_m5.csv", index=False)