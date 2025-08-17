from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv("./data/product_detail.csv")
# convert html description to raw description using bs4
df["description"] = df["description"].apply(
    lambda x: str(BeautifulSoup(x, "html.parser").get_text()).strip() if pd.notnull(x) and "Chưa có đánh giá nào" not in x else ""
)
df["product_name"] = df["product_name"].apply(
    lambda x: str(x).strip()
)
df.to_csv("./data/product_detail_clean.csv", index=False)