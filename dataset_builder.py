import time
import csv

DATA_FILE = "dataset.csv"

def save_row(row):
    header = [
        "price","ema20","ema50","rsi","macd","momentum","label"
    ]

    try:
        with open(DATA_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
    except:
        pass

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
