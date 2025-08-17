from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv("./data/product_detail.csv")
# convert html description to raw description using bs4
df["description"] = df["description"].apply(
    lambda x: BeautifulSoup(x, "html.parser").get_text() if pd.notnull(x) else ""
)

df.to_csv("./data/product_detail_clean.csv", index=False)