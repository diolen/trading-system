import pandas as pd
from datetime import timedelta

from app.models.signal import Signal
from app.config import settings


class SignalEngine:

    def __init__(self):
        self.last_signal_time = None

        self.breakout_state = None
        self.breakout_level = None
        self.last_breakout_level = None

        # =========================
        # RANGE STATE
        # =========================
        self.range_high = None
        self.range_low = None
        self.range_active = False
        self.range_created_time = None

    # =========================
    # ATR
    # =========================
    def calculate_atr(self, df: pd.DataFrame):
        high = df["high"]
        low = df["low"]
        close = df["close"]

        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)

        return tr.rolling(settings.ATR_PERIOD).mean()

    # =========================
    # LEVEL FILTER
    # =========================
    def is_same_level(self, level1, level2, atr):
        if level1 is None or level2 is None:
            return False

        return abs(level1 - level2) < atr * 0.2

    # =========================
    # RANGE BUILDER
    # =========================
    def build_range(self, df, current_time):
        recent = df.iloc[-settings.RANGE_PERIOD-1:-1]

        self.range_high = recent["high"].max()
        self.range_low = recent["low"].min()

        self.range_created_time = current_time
        self.range_active = True

    # =========================
    # RANGE VALIDATION
    # =========================
    def range_is_valid(self, current_time):
        if not self.range_active or self.range_created_time is None:
            return False

        return (current_time - self.range_created_time) < timedelta(minutes=200)

    # =========================
    # MAIN LOGIC
    # =========================
    def generate(self, df: pd.DataFrame) -> Signal | None:

        if len(df) < settings.RANGE_PERIOD + settings.ATR_PERIOD:
            return None

        df = df.copy()
        df["atr"] = self.calculate_atr(df)

        last = df.iloc[-1]
        current_time = last.name
        atr = last["atr"]

        if pd.isna(atr):
            return None

        # ===== COOLDOWN =====
        if self.last_signal_time:
            if current_time - self.last_signal_time < timedelta(minutes=50):
                return None

        # =========================================================
        # RANGE MANAGEMENT
        # =========================================================
        if not self.range_active or not self.range_is_valid(current_time):
            self.build_range(df, current_time)
            return None

        range_high = self.range_high
        range_low = self.range_low
        range_size = range_high - range_low

        if range_size < atr * settings.MIN_RANGE_ATR:
            return None

        # =========================================================
        # BREAKOUT DETECTION
        # =========================================================
        if self.breakout_state is None:

            if last["close"] > range_high:

                if self.is_same_level(range_high, self.last_breakout_level, atr):
                    return None

                self.breakout_state = "long"
                self.breakout_level = range_high
                return None

            if last["close"] < range_low:

                if self.is_same_level(range_low, self.last_breakout_level, atr):
                    return None

                self.breakout_state = "short"
                self.breakout_level = range_low
                return None

        # =========================================================
        # LONG ENTRY
        # =========================================================
        if self.breakout_state == "long":

            if last["low"] <= self.breakout_level and last["close"] > self.breakout_level:

                entry = float(last["close"])
                stop = self.breakout_level - atr * 0.5
                tp = entry + (entry - stop) * settings.RR

                self.last_signal_time = current_time
                self.last_breakout_level = self.breakout_level

                self.breakout_state = None
                self.breakout_level = None

                # reset range
                self.range_active = False
                self.range_high = None
                self.range_low = None

                return Signal(
                    pair=settings.PAIR,
                    direction="long",
                    entry=entry,
                    stop=float(stop),
                    tp=float(tp),
                    timestamp=current_time
                )

        # =========================================================
        # SHORT ENTRY
        # =========================================================
        if self.breakout_state == "short":

            if last["high"] >= self.breakout_level and last["close"] < self.breakout_level:

                entry = float(last["close"])
                stop = self.breakout_level + atr * 0.5
                tp = entry - (stop - entry) * settings.RR

                self.last_signal_time = current_time
                self.last_breakout_level = self.breakout_level

                self.breakout_state = None
                self.breakout_level = None

                # reset range
                self.range_active = False
                self.range_high = None
                self.range_low = None

                return Signal(
                    pair=settings.PAIR,
                    direction="short",
                    entry=entry,
                    stop=float(stop),
                    tp=float(tp),
                    timestamp=current_time
                )

        return None