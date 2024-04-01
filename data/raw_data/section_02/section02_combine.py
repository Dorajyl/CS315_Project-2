import pandas as pd
import os

# Initialize an empty dataframe
data = pd.DataFrame()

file_num = 3

def read_csv_files(folder):
    global data  # Use global keyword to modify the global data DataFrame
    global file_num
    # Iterate through each file in the folder
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            # Read the CSV file into a temporary dataframe
            temp_df = pd.read_csv(f"{folder}/{file}")
            
            # Adding data_user column to seperate by user easily
            if folder == "data/raw_data/section_02/chunks":
                temp_df["data_user"] = "user_0002"
            else:
                temp_df["data_user"] = f"user_000{file_num}"
                file_num += 1
            
            # Append the temporary dataframe to the combined dataframe
            data = pd.concat([data, temp_df], ignore_index=True)
            data = data.drop_duplicates()

# Combining chunks data first and then other sec02 users
chunks = "data/raw_data/section_02/chunks"
read_csv_files(chunks)

section_02 = "data/raw_data/section_02"
read_csv_files(section_02)

# Saving as csv
data.to_csv("data/raw_data/section_02.csv", index=False)
