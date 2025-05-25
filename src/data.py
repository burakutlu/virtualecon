# the t period is between 2024/11/27 - 2024/11/30, and i assume that there were no great volatility

# t basket -> Basket = sigma(P0,i*Q0,i)
# t+1 basket -> BasketT+1 = sigma(P1,i*Q1,i)

# prototype

import pandas as pd

df = pd.read_csv("/home/burak/Desktop/virtualecon-analysis/data/1_Pure_essence.csv", parse_dates=["date"])

df["weighted_price"] = df["price"] * df["quantity"]

monthly_data = df.groupby(pd.Grouper(key="date", freq="M")).agg(
    weighted_avg_price=("weighted_price", "sum"),
    total_quantity=("quantity", "sum"),
    simple_avg_price=("price", "mean")
).reset_index()

monthly_data["weighted_avg_price"] = monthly_data["weighted_avg_price"] / monthly_data["total_quantity"]

print(monthly_data[["date", "weighted_avg_price", "total_quantity"]])