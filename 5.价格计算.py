import pandas as pd

def main(stock_pd, stock, res_pd):
	
	stock_pd = stock_pd[file_pd["date"]>"2013-01-01"]



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


def save(res_pd):
	res_pd.to_csv("./股票关键数据/res.csv", encoding="gbk", index=False)

if __name__ == '__main__':

	stock_list = ["sz.000507", "sz.002269"]

	res_pd = pd.DataFrame(columns=("stock_code",'pbMRQ_min_down','pbMRQ_min_up','pbMRQ_max_down','pbMRQ_max_up','peTTM_min_down','peTTM_min_up','peTTM_max_down','peTTM_max_up',
							'psTTM_min_down','psTTM_min_up','psTTM_max_down','psTTM_max_up','pcfNcfTTM_min_down','pcfNcfTTM_min_up','pcfNcfTTM_max_down','pcfNcfTTM_max_up'))

	for stock in stock_list:

		file_pd = pd.read_csv("./res/"+stock+"_d.csv")
		res_pd = main(file_pd, stock, res_pd)

	save(res_pd)
	print(res_pd)
