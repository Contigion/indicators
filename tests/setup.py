import os
import pandas as pd


current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "resources", "data.csv")

data = pd.read_csv(csv_path)
n_candles = 499
