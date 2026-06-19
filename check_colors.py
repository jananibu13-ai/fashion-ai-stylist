import pandas as pd

df = pd.read_csv("data/styles.csv")

print(sorted(df["baseColour"].dropna().unique()))