import pandas as pd
from strategy.breakout import BreakoutStrategy

df = pd.read_csv("data_m5.csv", parse_dates=["time"])
df.set_index("time", inplace=True)

strategy = BreakoutStrategy()

signal = strategy.generate_signal(df, "EUR/GBP")

if signal:
    print(signal)
else:
    print("No signal")
