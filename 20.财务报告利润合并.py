import pandas as pd


def merge_data(code, total_code_list):
	stock_code_pd = pd.read_csv("./数据文件/股票财报表/"+code+".csv", encoding="gbk")
	# print(stock_code_pd["netProfit"].values)
	# print(stock_code_pd["MBRevenue"].values)
	res_list = stock_code_pd["netProfit"].values.tolist() + stock_code_pd["MBRevenue"].values.tolist()
	res_list.insert(0, code)
	# print(res_list)
	total_code_list.append(res_list)


def list2csv(total_code_list):

	columns = ["code", "2017NetProfit","2018NetProfit","2019NetProfit","2017TotalProfit","2018TotalProfit","2019TotalProfit"]
	result_pd = pd.DataFrame(total_code_list, columns=columns)

	result_pd["2018NetProfitMargin"] = (result_pd["2018NetProfit"] - result_pd["2017NetProfit"]) / result_pd["2017NetProfit"]
	result_pd["2019NetProfitMargin"] = (result_pd["2019NetProfit"] - result_pd["2018NetProfit"]) / result_pd["2018NetProfit"]

	# print(result_pd)

	result_pd.to_csv("./数据文件/股票财务报表利润合并/利润汇总_2021.csv", encoding="gbk", index=False)


def main():
	all_stock_code_pd = pd.read_csv("./数据文件/所有股票/baostock_all.csv", encoding="gbk")
	code_list = all_stock_code_pd["code"].values[:2]

	# print(code_list)

	total_code_list = []

	for code in code_list:
		merge_data(code, total_code_list)

	# print(total_code_list)
	list2csv(total_code_list)


if __name__ == '__main__':
	main()