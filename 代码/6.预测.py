import pandas as pd


#买入时间存储
def in_time(stock_pd, main_data, stock_code):
	#买入数值设置
	#pbMRQ: 1.79
	#peTTM: 0 < x < 30
	#psTTM：3.17
	#pcfNcfTTM： 0 < x <50

	print(stock_code)
	stock_data = main_data[main_data["stock_code"]==stock_code]

	in_pbMRQ = stock_data["in_pbMRQ"].values[0]
	in_psTTM = stock_data["in_psTTM"].values[0]
	in_peTTM_down = stock_data["in_pcfNcfTTM_down"].values[0]
	in_peTTM_up = stock_data["in_pcfNcfTTM_up"].values[0]
	in_pcfNcfTTM_down = stock_data["in_pcfNcfTTM_down"].values[0]
	in_pcfNcfTTM_up = stock_data["in_pcfNcfTTM_up"].values[0]
 
	in_time = stock_pd[
					(stock_pd["pbMRQ"] < in_pbMRQ)
					&(stock_pd["psTTM"] < in_psTTM)
					# &(stock_pd["peTTM"]>in_peTTM_down)
					# &(stock_pd["peTTM"]<in_peTTM_up)
					&(stock_pd["pcfNcfTTM"] > in_pcfNcfTTM_down)
					&(stock_pd["pcfNcfTTM"] < in_pcfNcfTTM_up)
					]

	# pbMRQ = stock_data["pbMRQ_min_up"].values[0]

	# psTTM = stock_data["psTTM_min_up"].values[0]

	

	# print(psTTM)


	# in_time = stock_pd[
	# 				(stock_pd["pbMRQ"] < pbMRQ)
	# 				&(stock_pd["psTTM"] < psTTM)
	# 				# &(stock_pd["peTTM"]<30)
	# 				# &(stock_pd["peTTM"]>0)
	# 				&(stock_pd["pcfNcfTTM"] > 0)
	# 				&(stock_pd["pcfNcfTTM"] < 50)
	# 				]

	# in_time = stock_pd[
	# 				(stock_pd["pbMRQ"]<1.79)
	# 				&(stock_pd["psTTM"]<3.17)
	# 				# &(stock_pd["peTTM"]<30)
	# 				# &(stock_pd["peTTM"]>0)
	# 				&(stock_pd["pcfNcfTTM"]>0)
	# 				&(stock_pd["pcfNcfTTM"]<50)
	# 				]


	# print(in_time)
	in_time.to_csv("./预测结果表/"+stock_code+"_in.csv", encoding="gbk", index=False)

#卖出时间存储
def out_time(stock_pd, main_data, stock_code):

	#买入数值设置
	#pbMRQ: x>3.3
	#peTTM: 0 < x < 30
	#psTTM：x>4.2
	#pcfNcfTTM： 0<x <50

	stock_data = main_data[main_data["stock_code"]==stock_code]

	out_pbMRQ = stock_data["out_pbMRQ"].values[0]
	out_psTTM = stock_data["out_psTTM"].values[0]
	out_peTTM_down = stock_data["out_pcfNcfTTM_down"].values[0]
	out_peTTM_up = stock_data["out_pcfNcfTTM_up"].values[0]
	out_pcfNcfTTM_down = stock_data["out_pcfNcfTTM_down"].values[0]
	out_pcfNcfTTM_up = stock_data["out_pcfNcfTTM_up"].values[0]

	out_time = stock_pd[
				(stock_pd["pbMRQ"] > out_pbMRQ)
				&(stock_pd["psTTM"] > out_psTTM)
				# &(stock_pd["peTTM"] > out_peTTM_down)
				# &(stock_pd["peTTM"] < out_peTTM_up)
				# &(stock_pd["pcfNcfTTM"] > out_pcfNcfTTM_down)
				# &(stock_pd["pcfNcfTTM"] < out_pcfNcfTTM_up)
				]

	# pbMRQ = round((stock_data["pbMRQ_max_up"].values[0] + stock_data["pbMRQ_max_down"].values[0])/2, 2)

	# psTTM = round((stock_data["psTTM_max_up"].values[0] + stock_data["psTTM_max_down"].values[0])/2, 2)
	
	# print(pbMRQ)
	# print(psTTM)

	# out_time = stock_pd[
	# 		(stock_pd["pbMRQ"] > pbMRQ)
	# 		&(stock_pd["psTTM"] > psTTM)
	# 		# &(stock_pd["peTTM"]<30)
	# 		# &(stock_pd["peTTM"]>0)
	# 		# &(stock_pd["pcfNcfTTM"]>0)
	# 		# &(stock_pd["pcfNcfTTM"]<50)
	# 		]

	# out_time = stock_pd[
	# 			(stock_pd["pbMRQ"] > 3.3)
	# 			&(stock_pd["psTTM"] > 4.2)
	# 			# &(stock_pd["peTTM"]<30)
	# 			# &(stock_pd["peTTM"]>0)
	# 			# &(stock_pd["pcfNcfTTM"]>0)
	# 			# &(stock_pd["pcfNcfTTM"]<50)
	# 			]

	# print(out_time)
	out_time.to_csv("./预测结果表/"+stock_code+"_out.csv", encoding="gbk", index=False)


if __name__ == '__main__':
	
	# stock_code = "sz.000507"
	# stock_code = "sz.002269"

	# all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	# stock_code_list = all_stock_code_pd["code"].values

	all_stock_code_pd = pd.read_csv("./股票关键数据/true.csv", encoding="gbk")
	stock_code_list = all_stock_code_pd["stock_code"].values

	# print(stock_code_list)

	for stock_code in stock_code_list:
		stock_pd = pd.read_csv("./数据合并处理/"+stock_code+"_day_qfq_c.csv")
		stock_pd = stock_pd[stock_pd["date"]>"2013-01-01"]

		main_data = pd.read_csv("./股票关键数据/true.csv")

		# print(stock_pd)

		in_time(stock_pd, main_data, stock_code)

		out_time(stock_pd, main_data, stock_code)

	print("END")
