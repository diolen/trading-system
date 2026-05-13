import sys
import os
import pandas as pd

# важно: добавляем корень проекта в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.strategy.breakout import BreakoutStrategy


def main():
    df = pd.read_csv("data_m5.csv", parse_dates=["time"])
    df.set_index("time", inplace=True)

    strategy = BreakoutStrategy()

    signal = strategy.generate_signal(df, "EUR/GBP")

    if signal:
        print("SIGNAL:")
        print(signal)
    else:
        print("No signal")


if __name__ == "__main__":
    main()