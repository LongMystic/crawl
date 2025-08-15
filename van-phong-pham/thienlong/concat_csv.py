import pandas as pd

df1 = pd.read_csv("./data/product_detail_250.csv")
df2 = pd.read_csv("./data/product_detail_500.csv")
df3 = pd.read_csv("./data/product_detail_750.csv")

df = pd.concat([df1, df2, df3], axis=0)

df.to_csv("./data/product_detail.csv", index=False)