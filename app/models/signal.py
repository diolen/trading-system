from dataclasses import dataclass
from datetime import datetime


@dataclass
class Signal:
    pair: str
    direction: str
    entry: float
    stop: float
    tp: float
    timestamp: datetime

    def __post_init__(self):
        self.entry = round(float(self.entry), 5)
        self.stop = round(float(self.stop), 5)
        self.tp = round(float(self.tp), 5)