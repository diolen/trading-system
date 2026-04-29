import requests
import lzma
import pandas as pd
from datetime import datetime, timedelta
import struct


BASE_URL = "https://datafeed.dukascopy.com/datafeed/EURGBP"


def download_hour(year, month, day, hour):
    url = f"{BASE_URL}/{year}/{month-1:02d}/{day:02d}/{hour:02d}h_ticks.bi5"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None

        data = lzma.decompress(r.content)
        return data
    except:
        return None


def parse_ticks(data, date, hour):
    ticks = []
    size = 20

    for i in range(0, len(data), size):
        chunk = data[i:i+size]
        if len(chunk) < size:
            continue

        ms, bid, ask, bid_vol, ask_vol = struct.unpack(">IIIff", chunk)
        timestamp = date + timedelta(hours=hour, milliseconds=ms)
        price = bid / 100000
        volume = bid_vol + ask_vol
        ticks.append([timestamp, price, price, price, price, volume])

    return ticks


def download_day(date):
    all_ticks = []

    for hour in range(24):
        raw = download_hour(date.year, date.month, date.day, hour)
        if raw:
            ticks = parse_ticks(raw, date, hour)
            all_ticks.extend(ticks)

    df = pd.DataFrame(all_ticks, columns=["time", "open", "high", "low", "close", "volume"])
    return df


def to_m5(df):
    df.set_index("time", inplace=True)

    m5 = df.resample("5min").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()

    return m5.reset_index()


if __name__ == "__main__":
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 3)

    all_days = []

    current = start
    while current <= end:
        print(f"Downloading {current.date()}...")
        df_day = download_day(current)
        all_days.append(df_day)
        current += timedelta(days=1)

    df = pd.concat(all_days)

    df_m5 = to_m5(df)

    df_m5.to_csv("data/data_m5.csv", index=False)
    print("Saved data/data_m5.csv")