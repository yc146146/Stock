import pandas as pd
import time
def main(stock_pd, stock, res_pd, all_stock_code_pd):
	
	stock_pd = stock_pd[file_pd["date"]>"2013-01-01"]

	stock_industry = all_stock_code_pd[all_stock_code_pd["code"] == stock]["industry"]

	price_max = stock_pd["stock_second_close"].max()
	price_min = stock_pd["stock_second_close"].min()

	#按年找最大和最小
	year_price_max_list = []
	year_price_min_list = []

	year_price_max_pd = "";
	year_price_min_pd = "";

	for y in range(13,21):
		stock_pd_temp = stock_pd[(stock_pd["date"]>"20"+str(y)+"-01-01") & (stock_pd["date"]<"20"+str(y+1)+"-12-31")]
		max_temp = stock_pd_temp["stock_second_close"].max()
		min_temp = stock_pd_temp["stock_second_close"].min()
		max_info_temp = stock_pd_temp[stock_pd_temp["stock_second_close"]==max_temp][0:1]
		min_info_temp = stock_pd_temp[stock_pd_temp["stock_second_close"]==min_temp][0:1]


		if y==13:
			year_price_max_pd = max_info_temp
			year_price_min_pd = min_info_temp
		else:
			year_price_max_pd = pd.concat([year_price_max_pd, max_info_temp],ignore_index=True)
			year_price_min_pd = pd.concat([year_price_min_pd, min_info_temp],ignore_index=True)

		# print(max_info_temp)
		# year_price_max_list.append(max_temp)
		# year_price_max_list.append(max_info_temp)
		# year_price_min_list.append(min_temp)
		# year_price_min_list.append(min_temp)




	# res = stock_000507[stock_000507["stock_second_close"]==price_min]

	# print(price_min)
	# print(price_max)
	# print(year_price_min_list)
	# print(year_price_max_list)

	year_price_min_max = year_price_min_pd[["stock_second_close"]].max()

	year_price_max_pd = year_price_max_pd[year_price_max_pd["stock_second_close"] > year_price_min_max.squeeze()]

	year_price_min_pd = year_price_min_pd[year_price_min_pd["stock_second_close"] < year_price_min_max.squeeze()]

	# print(year_price_max_pd[["date","stock_second_close","pcfNcfTTM"]])
	# print(year_price_min_pd[["date","stock_second_close","pcfNcfTTM"]])

	# print(year_price_max_pd["pbMRQ"].max())
	# print(year_price_max_pd["pbMRQ"].min())
	# print(year_price_min_pd["pbMRQ"].max())
	# print(year_price_min_pd["pbMRQ"].min())

	# print(year_price_max_pd["peTTM"].max())
	# print(year_price_max_pd["peTTM"].min())
	# print(year_price_min_pd["peTTM"].max())
	# print(year_price_min_pd["peTTM"].min())

	# print(year_price_max_pd["psTTM"].max())
	# print(year_price_max_pd["psTTM"].min())
	# print(year_price_min_pd["psTTM"].max())
	# print(year_price_min_pd["psTTM"].min())

	# print(year_price_max_pd["pcfNcfTTM"].max())
	# print(year_price_max_pd["pcfNcfTTM"].min())
	# print(year_price_min_pd["pcfNcfTTM"].max())
	# print(year_price_min_pd["pcfNcfTTM"].min())




	stock_item = {
			 "stock_code": stock,
			 "stock_industry": stock_industry,
			 'pbMRQ_min_down': [year_price_min_pd["pbMRQ"].min()],
  			 'pbMRQ_min_up': [year_price_min_pd["pbMRQ"].max()],
  			 'pbMRQ_max_down': [year_price_max_pd["pbMRQ"].min()],
  			 'pbMRQ_max_up': [year_price_max_pd["pbMRQ"].max()],

  			 'peTTM_min_down': [year_price_min_pd["peTTM"].min()],
  			 'peTTM_min_up': [year_price_min_pd["peTTM"].max()],
  			 'peTTM_max_down': [year_price_max_pd["peTTM"].min()],
  			 'peTTM_max_up': [year_price_max_pd["peTTM"].max()],

  			 'psTTM_min_down': [year_price_min_pd["psTTM"].min()],
  			 'psTTM_min_up': [year_price_min_pd["psTTM"].max()],
  			 'psTTM_max_down': [year_price_max_pd["psTTM"].min()],
  			 'psTTM_max_up':[year_price_max_pd["psTTM"].max()],

  			 'pcfNcfTTM_min_down': [year_price_min_pd["pcfNcfTTM"].min()],
  			 'pcfNcfTTM_min_up': [year_price_min_pd["pcfNcfTTM"].max()],
  			 'pcfNcfTTM_max_down': [year_price_max_pd["pcfNcfTTM"].min()],
  			 'pcfNcfTTM_max_up': [year_price_max_pd["pcfNcfTTM"].max()]
  			 }

	# res_pd = pd.DataFrame({
	#   '000507': {'pbMRQ_min_down': year_price_max_pd["pbMRQ"].min(),
	#   			 'pbMRQ_min_up': year_price_max_pd["pbMRQ"].max(),
	#   			 'pbMRQ_max_down': year_price_min_pd["pbMRQ"].min(),
	#   			 'pbMRQ_max_up': year_price_min_pd["pbMRQ"].max(),

	#   			 'peTTM_min_down': year_price_max_pd["peTTM"].min(),
	#   			 'peTTM_min_up': year_price_max_pd["peTTM"].max(),
	#   			 'peTTM_max_down': year_price_min_pd["peTTM"].min(),
	#   			 'peTTM_max_up': year_price_min_pd["peTTM"].max(),

	#   			 'psTTM_min_down': year_price_max_pd["psTTM"].min(),
	#   			 'psTTM_min_up': year_price_max_pd["psTTM"].max(),
	#   			 'psTTM_max_down': year_price_min_pd["psTTM"].min(),
	#   			 'psTTM_max_up': year_price_min_pd["psTTM"].max(),

	#   			 'pcfNcfTTM_min_down': year_price_max_pd["pcfNcfTTM"].max(),
	#   			 'pcfNcfTTM_min_up': year_price_max_pd["pcfNcfTTM"].min(),
	#   			 'pcfNcfTTM_max_down': year_price_min_pd["pcfNcfTTM"].max(),
	#   			 'pcfNcfTTM_max_up': year_price_min_pd["pcfNcfTTM"].min()
	#   			 },
	# })

	res_pd = res_pd.append(pd.DataFrame(stock_item))

	return res_pd

def analysis(res_pd):

	res_pd["in_pbMRQ"] = res_pd["pbMRQ_min_up"]
	res_pd["in_psTTM"] = res_pd["psTTM_min_up"]

	res_pd["in_peTTM_down"] = 0
	res_pd["in_peTTM_up"] = 30

	res_pd["in_pcfNcfTTM_down"] = 0
	res_pd["in_pcfNcfTTM_up"] = 50

	res_pd["out_pbMRQ"] = res_pd.apply(lambda x:round((x["pbMRQ_max_up"] + x["pbMRQ_max_down"])/2, 2), axis=1)
	res_pd["out_psTTM"] = res_pd.apply(lambda x:round((x["psTTM_max_up"] + x["psTTM_max_down"])/2, 2), axis=1) 


	res_pd["out_peTTM_down"] = 50
	res_pd["out_peTTM_up"] = 100

	res_pd["out_pcfNcfTTM_down"] = 60
	res_pd["out_pcfNcfTTM_up"] = 120


	res_pd["pbMRQ_error"] = res_pd["out_pbMRQ"] < res_pd["in_pbMRQ"]
	res_pd["psTTM_error"] = res_pd["out_psTTM"] < res_pd["in_psTTM"]

	#市净率 和 市销率 都正确 保存到正确结果
	true_pd = res_pd[(res_pd["pbMRQ_error"]==False) & (res_pd["psTTM_error"]==False)]

	#市净率 和 市销率 存在任何一项是错的 保存到错误结果
	err_pd = res_pd[(res_pd["pbMRQ_error"]==True) | (res_pd["psTTM_error"]==True)]

	return true_pd,err_pd


def save(true_pd, err_pd):
	# date = time.strftime("%Y-%m-%d")

	# res_pd.to_csv("./股票关键数据/"+date+".csv", encoding="gbk", index=False)
	true_pd.to_csv("./股票关键数据/true.csv", encoding="gbk", index=False)
	err_pd.to_csv("./股票关键数据/error.csv", encoding="gbk", index=False)

if __name__ == '__main__':

	# stock_code_list = ["sz.000507", "sz.002269"]

	all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	stock_code_list = all_stock_code_pd["code"].values

	res_pd = pd.DataFrame(columns=("stock_code", 'stock_industry','pbMRQ_min_down','pbMRQ_min_up','pbMRQ_max_down','pbMRQ_max_up','peTTM_min_down','peTTM_min_up','peTTM_max_down','peTTM_max_up',
							'psTTM_min_down','psTTM_min_up','psTTM_max_down','psTTM_max_up','pcfNcfTTM_min_down','pcfNcfTTM_min_up','pcfNcfTTM_max_down','pcfNcfTTM_max_up'))

	for stock_code in stock_code_list:

		file_pd = pd.read_csv("./数据合并处理/"+stock_code+"_day_qfq_c.csv")
		res_pd = main(file_pd, stock_code, res_pd, all_stock_code_pd)


	true_pd,err_pd = analysis(res_pd)

	save(true_pd, err_pd)
	print(res_pd)
