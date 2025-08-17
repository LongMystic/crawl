import pandas as pd

df = pd.read_csv("data/product_detail.csv")

df["product_name"] = df["product_name"].str.strip()

df.to_csv("./data/product_detail_clean.csv", index=False)