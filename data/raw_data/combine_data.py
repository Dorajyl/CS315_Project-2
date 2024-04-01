import pandas as pd

# Adding original data as user_0001
original = pd.read_csv("data/raw_data/original_data.csv")
original["data_user"] = "user_0001"

section_02 = pd.read_csv("data/raw_data/section_02.csv")

# Joining together both datasets and deleting any possible duplicates
data = pd.concat([original, section_02], ignore_index=True)
data = data.drop_duplicates()

# Checking that we have 7 users
print(data['data_user'].drop_duplicates().values)

# Saving as csv
data.to_csv("data/metadata.csv", index=False)