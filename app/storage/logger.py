import csv
from app.models.signal import Signal


def log_signal(signal: Signal, path="signals.csv"):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            signal.timestamp,
            signal.pair,
            signal.direction,
            signal.entry,
            signal.stop,
            signal.tp
        ])
