import pandas as pd



def main(stock_code):
	# stock_code = "sz.002269"
	stock_pd = pd.read_csv("./数据文件/baostock_data/股票/"+stock_code+"_day_qfq.csv", encoding="gbk")

	# print(stock_pd.head())

	industry = stock_pd["industry"].iloc[0]

	# print(industry)

	industry_pd = pd.read_csv("./数据文件/行业数据分析/历史交易时间线研究/"+industry+".csv", encoding="gbk")

	# print(industry_pd.head()) 

	columns = {
	"pbMRQ_mean":"industry_pbMRQ_mean",
	"peTTM_mean":"industry_peTTM_mean",
	"peTTM_median":"industry_peTTM_median",
	"psTTM_mean":"industry_psTTM_mean",
	"pcfNcfTTM_mean":"industry_pcfNcfTTM_mean",
	}

	stock_pd = stock_pd[["date", "code", "industry", "close", "pbMRQ", "peTTM", "psTTM", "pcfNcfTTM"]]

	industry_pd = industry_pd[["date",  "pbMRQ_mean", "peTTM_mean", "peTTM_median", "psTTM_mean", "pcfNcfTTM_mean"]]
	industry_pd.rename(columns=columns, inplace=True)


	merge_date_pd = pd.merge(stock_pd, industry_pd, how="inner", on="date")

	# print(merge_date_pd.head())

	#排序数据
	date_list = merge_date_pd["date"].values

	# print(date_list)

	industry_sort_item_list = []
	for date in date_list:

		industry_day_pd = pd.read_csv("./数据文件/行业数据分析/历史/"+date+".csv", encoding="gbk")

		industry_day_pd.set_index("industry", drop=True, inplace=True)

		# 交易量排序
		industry_volume_sort = industry_day_pd['volume_mean'].sort_values(ascending=False).index

		industry_volume_item = {}
		for i, industry_temp in enumerate(industry_volume_sort):
			industry_volume_item[industry_temp] = i+1

		industry_peTTM_median_sort = industry_day_pd['peTTM_median'].sort_values(ascending=False).index

		industry_peTTM_median_item = {}
		for i, industry_temp in enumerate(industry_peTTM_median_sort):
			industry_peTTM_median_item[industry_temp] = i+1

		industry_sort_item = {}
		industry_sort_item["date"] = date
		industry_sort_item["industry_volume_sort"] = industry_volume_item[industry]
		industry_sort_item["industry_pbMRQ_mean_sort"] = industry_peTTM_median_item[industry]
		industry_sort_item_list.append(industry_sort_item)

	# print(industry_sort_item_list)

	#排序pd文件
	sort_pd = pd.DataFrame(industry_sort_item_list, columns=["date","industry_volume_sort","industry_pbMRQ_mean_sort"])

	# print(sort_pd)

	merge_date_pd = pd.merge(merge_date_pd, sort_pd, how="inner", on="date")

	print(merge_date_pd)

	merge_date_pd.to_csv("./数据文件/深度学习文件/"+stock_code+".csv", encoding="gbk", index=False)


if __name__ == '__main__':

	stock_list = [
	"sh.600000",
	"sh.600004",
	"sh.600006",
	"sh.600007",
	"sh.600008",
	"sz.000001",
	"sz.000002",
	"sz.000004",
	"sz.000005",
	"sz.000006",
	]

	print("开始")
	for stock in stock_list:
		main(stock)

	print("结束")