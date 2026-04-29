class SignalEngine:

    def __init__(self):
        # ======================
        # COOLDOWN
        # ======================
        self.last_signal_time = None

        # ======================
        # RANGE STATE
        # ======================
        self.range_high = None
        self.range_low = None
        self.range_start_time = None
        self.range_ready = False

        # ======================
        # BREAKOUT STATE
        # ======================
        self.breakout_state = None   # None / "long" / "short"
        self.breakout_level = None

        # ======================
        # TRADE FILTERS
        # ======================
        self.last_direction = None
        self.last_breakout_level = None