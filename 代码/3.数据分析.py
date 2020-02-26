import pandas as pd




def main(stock_code, stock_main_sz_pd, stock_main_sh_pd, stock_pd):

	stock_address = stock_code.split(".")[0]
	# print(stock_address)

	if stock_address == "sh":
		stock_main_pd = stock_main_sh_pd
		
	else:
		stock_main_pd = stock_main_sz_pd

	main = stock_main_pd[["date","close"]].copy()
	main.rename(columns={"close":"stock_main_close"}, inplace=True)
	main.set_index("date", inplace=True)


	second = stock_pd[["date","industry","close","pbMRQ","peTTM","psTTM","pcfNcfTTM"]].copy()
	second.rename(columns={"close":"stock_second_close"}, inplace=True)
	# second.set_index("date", inplace=True)

	res = pd.merge(main, second, how="inner", on="date")

	# print(res.head())




	res.to_csv("./数据合并处理/"+stock_code+"_day_qfq_c.csv", encoding="gbk", index=False)




if __name__ == '__main__':
	stock_main_sz_pd = pd.read_csv("./baostock_data/指数/sz.399106_day.csv", encoding="gbk")
	stock_main_sh_pd = pd.read_csv("./baostock_data/指数/sh.000001_day.csv", encoding="gbk")

	# stock_second_list = ["sz.002269", "sz.000507"]

	all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	stock_second_list = all_stock_code_pd["code"].values

	# stock_002269 = pd.read_csv("./baostock_data/sz.002269_day_qfq.csv")
	# stock_000507 = pd.read_csv("./baostock_data/sz.000507_day_qfq.csv")

	for stock_code in stock_second_list:

		stock_pd = pd.read_csv("./baostock_data/股票/"+stock_code+"_day_qfq.csv", encoding="gbk")
		main(stock_code, stock_main_sz_pd, stock_main_sh_pd, stock_pd)