import pandas as pd

original = pd.read_csv('temp.csv', usecols=["Date", "County", "O3_Mean", "CO_Mean", "SO2_Mean", "NO2_Mean"])
filtered = original[original['Date'].str.contains("-01-01")]
print(filtered)
filtered.to_csv("temp_filtered.csv", index=False)
