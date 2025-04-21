
import pandas as pd

df = pd.read_csv("static/table_01_71q113.csv")
df = df.drop(df.columns[[1, 5, 6, 7, 8, 10, 11, 12, 13, 26, 27, 28, 29]], axis=1)

df = df.drop(index=range(101, 121))


df["Urban_area"] = df["Urban_area"].str.split(",")
df["Urban_area"] = df["Urban_area"].str[0]

df["Urban_area"] = df["Urban_area"].str.upper()

years = [1982, 1985, 1990, 1995] + list(range(2000, 2012))

for year in years:
        df[str(year)] = df[str(year)].astype(str).str.replace("(R) ", "", regex=False)

df.to_csv("static/congestion_filtered.csv", index=False)

print(df)
df_transposed = df.T
print(df_transposed)
df_transposed.to_csv("static/congestion_filtered_transposed.csv", index=False)
