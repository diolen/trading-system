import pandas as pd
from datetime import timedelta

from app.models.signal import Signal
from app.config import settings


class SignalEngine:

    def __init__(self):
        self.last_signal_time = None

        # breakout state
        self.breakout_state = None  # "long" / "short"
        self.breakout_level = None
        self.breakout_time = None

        # anti-repeat
        self.used_levels = []  # [(level, time)]

        # range state
        self.range_high = None
        self.range_low = None
        self.range_active = False
        self.range_created_time = None

    # =========================
    # LEVEL FILTER (старый оставляем для других задач)
    # =========================
    def is_same_level(self, level1, level2):
        if level1 is None or level2 is None:
            return False

        return abs(level1 - level2) < settings.RETEST_TOLERANCE

    # =========================
    # ANTI-REPEAT
    # =========================
    def is_used_level(self, level, current_time):
        for lvl, t in self.used_levels:
            if abs(level - lvl) < settings.ANTI_REPEAT_TOLERANCE:
                return True
        return False

    def clean_levels(self, current_time):
        self.used_levels = [
            (lvl, t)
            for lvl, t in self.used_levels
            if (current_time - t) < timedelta(minutes=settings.LEVEL_EXPIRY_MINUTES)
        ]

    # =========================
    # RANGE BUILDER
    # =========================
    def build_range(self, df, current_time):
        recent = df.iloc[-settings.RANGE_CANDLES-1:-1]

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
    # SESSION FILTER (🔥 исправлено)
    # =========================
    def session_allowed(self, current_time):
        return settings.SESSION_START <= current_time.hour < settings.SESSION_END

    # =========================
    # MAIN LOGIC
    # =========================
    def generate(self, df: pd.DataFrame) -> Signal | None:

        if len(df) < settings.RANGE_CANDLES:
            return None

        last = df.iloc[-1]
        current_time = last.name

        # 🔥 чистим старые уровни
        self.clean_levels(current_time)

        # ===== SESSION FILTER =====
        if not self.session_allowed(current_time):
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

        if range_size < settings.MIN_RANGE_SIZE:
            return None

        # =========================================================
        # BREAKOUT DETECTION
        # =========================================================
        if self.breakout_state is None:

            avg_size = (df["high"] - df["low"]).rolling(10).mean().iloc[-1]
            current_size = last["high"] - last["low"]

            if current_size < avg_size:
                return None

            # LONG breakout
            if last["close"] > range_high:

                if self.is_used_level(range_high, current_time):
                    return None

                self.breakout_state = "long"
                self.breakout_level = range_high
                self.breakout_time = current_time
                return None

            # SHORT breakout
            if last["close"] < range_low:

                if self.is_used_level(range_low, current_time):
                    return None

                self.breakout_state = "short"
                self.breakout_level = range_low
                self.breakout_time = current_time
                return None

        # =========================================================
        # RETEST TIMEOUT
        # =========================================================
        if self.breakout_time:
            if current_time - self.breakout_time > timedelta(minutes=15 * settings.RETEST_MAX_CANDLES):
                self.breakout_state = None
                self.breakout_level = None
                self.breakout_time = None
                return None

        # =========================================================
        # LONG ENTRY
        # =========================================================
        if self.breakout_state == "long":

            if last["low"] <= self.breakout_level and last["close"] > self.breakout_level:

                retest_depth = self.breakout_level - last["low"]
                if retest_depth > range_size * settings.RETEST_DEPTH:
                    return None

                entry = float(last["close"])
                stop = self.breakout_level - settings.SL_BUFFER
                tp = entry + (entry - stop) * settings.RR_RATIO

                signal = Signal(
                    pair=settings.PAIR,
                    direction="long",
                    entry=entry,
                    stop=float(stop),
                    tp=float(tp),
                    timestamp=current_time
                )

                print(f"""
TIME: {current_time}

RANGE:
LOW: {range_low:.5f}
HIGH: {range_high:.5f}
SIZE: {range_size:.5f}

BREAKOUT: LONG

ENTRY: {entry}
SL: {stop}
TP: {tp}
""")

                self.last_signal_time = current_time
                self.used_levels.append((self.breakout_level, current_time))

                # reset
                self.breakout_state = None
                self.breakout_level = None
                self.breakout_time = None

                self.range_active = False
                self.range_high = None
                self.range_low = None

                return signal

        # =========================================================
        # SHORT ENTRY
        # =========================================================
        if self.breakout_state == "short":

            if last["high"] >= self.breakout_level and last["close"] < self.breakout_level:

                retest_depth = last["high"] - self.breakout_level
                if retest_depth > range_size * settings.RETEST_DEPTH:
                    return None

                entry = float(last["close"])
                stop = self.breakout_level + settings.SL_BUFFER
                tp = entry - (stop - entry) * settings.RR_RATIO

                signal = Signal(
                    pair=settings.PAIR,
                    direction="short",
                    entry=entry,
                    stop=float(stop),
                    tp=float(tp),
                    timestamp=current_time
                )

                print(f"""
TIME: {current_time}

RANGE:
LOW: {range_low:.5f}
HIGH: {range_high:.5f}
SIZE: {range_size:.5f}

BREAKOUT: SHORT

ENTRY: {entry}
SL: {stop}
TP: {tp}
""")

                self.last_signal_time = current_time
                self.used_levels.append((self.breakout_level, current_time))

                # reset
                self.breakout_state = None
                self.breakout_level = None
                self.breakout_time = None

                self.range_active = False
                self.range_high = None
                self.range_low = None

                return signal

        return None