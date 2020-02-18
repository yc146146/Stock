import pandas as pd


stock_399106 = pd.read_csv("./baostock_data/sz.399106_day.csv")
stock_002269 = pd.read_csv("./baostock_data/sz.002269_d.csv")
stock_000507 = pd.read_csv("./baostock_data/sz.000507_d.csv")


main = stock_399106[["date","close"]]
main.rename(columns={"close":"stock_main_close"}, inplace=True)
main.set_index("date", inplace=True)


second = stock_000507[["date","close","pbMRQ","peTTM","psTTM","pcfNcfTTM"]]
second.rename(columns={"close":"stock_second_close"}, inplace=True)
second.set_index("date", inplace=True)

res = pd.merge(main, second, how="inner", on="date")

print(res.head())




res.to_csv("./res/sz.000507_d.csv")