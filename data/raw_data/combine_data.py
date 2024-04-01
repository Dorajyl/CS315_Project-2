import pandas as pd

original = pd.read_csv("data/raw_data/original_data.csv")
original["data_user"] = "user_0001"

section_02 = pd.read_csv("data/raw_data/section_02.csv")

data = pd.concat([original, section_02], ignore_index=True)

data.to_csv("data/metadata.csv", index=False)