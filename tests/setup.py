import os
from pandas import read_csv


current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "resources", "data.csv")

data = read_csv(csv_path)
n_candles = 499
