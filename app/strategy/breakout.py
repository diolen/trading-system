from dataclasses import dataclass
import pandas as pd


@dataclass
class Signal:
    pair: str
    direction: str  # "long" or "short"
    entry: float
    stop: float
    tp: float
    range_high: float
    range_low: float
    range_size: float
    atr: float
    timestamp: pd.Timestamp


class BreakoutStrategy:

    def __init__(
        self,
        range_period: int = 24,   # 24 свечи M5 = ~2 часа
        atr_period: int = 14,
        atr_multiplier: float = 0.5,
        rr: float = 1.5,
        min_range_atr: float = 0.7,  # фильтр узкого флета
    ):
        self.range_period = range_period
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.rr = rr
        self.min_range_atr = min_range_atr

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        high = df["high"]
        low = df["low"]
        close = df["close"]

        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)

        return tr.rolling(self.atr_period).mean()

    def detect_range(self, df: pd.DataFrame):
        recent = df.iloc[-self.range_period:]
        range_high = recent["high"].max()
        range_low = recent["low"].min()
        range_size = range_high - range_low
        return range_high, range_low, range_size

    def is_valid_range(self, range_size: float, atr: float) -> bool:
        return range_size >= atr * self.min_range_atr

    def is_volatility_expanding(self, df: pd.DataFrame) -> bool:
        # простая логика: ATR растёт последние 3 свечи
        atr = df["atr"]
        return atr.iloc[-1] > atr.iloc[-2] > atr.iloc[-3]

    def generate_signal(self, df: pd.DataFrame, pair: str) -> Signal | None:

        if len(df) < self.range_period + self.atr_period + 3:
            return None

        df = df.copy()
        df["atr"] = self.calculate_atr(df)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        range_high, range_low, range_size = self.detect_range(df)
        atr = last["atr"]

        if pd.isna(atr):
            return None

        # ❌ фильтр узкого флета
        if not self.is_valid_range(range_size, atr):
            return None

        # ❌ фильтр волатильности
        if not self.is_volatility_expanding(df):
            return None

        buffer = atr * self.atr_multiplier

        # "свежий" breakout
        broke_up_now = prev["close"] <= range_high and last["close"] > range_high + buffer
        broke_down_now = prev["close"] >= range_low and last["close"] < range_low - buffer

        # 🔼 LONG
        if broke_up_now:
            entry = last["close"]
            stop = range_low
            risk = entry - stop
            tp = entry + risk * self.rr

            return Signal(
                pair=pair,
                direction="long",
                entry=entry,
                stop=stop,
                tp=tp,
                range_high=range_high,
                range_low=range_low,
                range_size=range_size,
                atr=atr,
                timestamp=last.name
            )

        # 🔽 SHORT
        if broke_down_now:
            entry = last["close"]
            stop = range_high
            risk = stop - entry
            tp = entry - risk * self.rr

            return Signal(
                pair=pair,
                direction="short",
                entry=entry,
                stop=stop,
                tp=tp,
                range_high=range_high,
                range_low=range_low,
                range_size=range_size,
                atr=atr,
                timestamp=last.name
            )

        return None
