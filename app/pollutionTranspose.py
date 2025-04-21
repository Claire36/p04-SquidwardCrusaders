import numpy as np
import pandas as pd

df = pd.read_csv("static/pollution_2000_2023_filtered.csv")

tdf = df.drop("Date", axis=1)
tdf = tdf.T

counties = []
for i in range(1600, -1, -1):
	county = tdf.iloc[0, i]
	repeated = county in counties
	if not repeated:
		counties.append(county);
	else:
		tdf = tdf.drop(tdf.columns[i], axis=1)
print(tdf)

data = {"year": list(range(2000, 2024))}
dfO3 = pd.DataFrame(columns=counties)
dfCO = pd.DataFrame(columns=counties)
dfSO2 = pd.DataFrame(columns=counties)
dfNO2 = pd.DataFrame(columns=counties)

dfO3.insert(0, "year", list(range(2000, 2024)))
dfCO.insert(0, "year", list(range(2000, 2024)))
dfSO2.insert(0, "year", list(range(2000, 2024)))
dfNO2.insert(0, "year", list(range(2000, 2024)))

for index, row in df.iterrows():
	yr = row["Date"]
	yr = int(yr[:4])
	newRow = yr-2000
	county = row["County"]
	dfO3.loc[newRow, county] = row["O3_Mean"]
	dfCO.loc[newRow, county] = row["CO_Mean"]
	dfSO2.loc[newRow, county] = row["SO2_Mean"]
	dfNO2.loc[newRow, county] = row["NO2_Mean"]

dfO3 = dfO3.replace(np.nan, 0)
dfCO = dfCO.replace(np.nan, 0)
dfSO2 = dfSO2.replace(np.nan, 0)
dfNO2 = dfNO2.replace(np.nan, 0)

dfO3.to_csv("./static/pollution_O3.csv", index=False)
dfCO.to_csv("./static/pollution_CO.csv", index=False)
dfSO2.to_csv("./static/pollution_SO2.csv", index=False)
dfNO2.to_csv("./static/pollution_NO2.csv", index=False)
