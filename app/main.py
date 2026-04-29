from app.data.data_provider import load_csv
from app.strategy.signal_engine import SignalEngine
from app.storage.logger import log_signal

engine = SignalEngine()

df = load_csv("data/data_m5.csv")

for i in range(len(df)):
    sub_df = df.iloc[:i+1]
    signal = engine.generate(sub_df)
    # print("Rows in DF:", len(df))
    # print(df.head())    

    if signal:
        print("SIGNAL:", signal)
        log_signal(signal)