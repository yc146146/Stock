import pandas as pd
import datetime
import numpy as np



#买入时机
def in_time(stock_pd, main_data, stock_code):

	# stock_code = stock_pd["code"]

	# print(stock_code)

	#买入数值设置
	stock_data = main_data[main_data["stock_code"]==stock_code]

	in_pbMRQ = stock_data["in_pbMRQ"].values[0]
	in_psTTM = stock_data["in_psTTM"].values[0]
	in_peTTM_down = stock_data["in_pcfNcfTTM_down"].values[0]
	in_peTTM_up = stock_data["in_pcfNcfTTM_up"].values[0]
	in_pcfNcfTTM_down = stock_data["in_pcfNcfTTM_down"].values[0]
	in_pcfNcfTTM_up = stock_data["in_pcfNcfTTM_up"].values[0]


	# print(float(stock_pd["pcfNcfTTM"])< in_pcfNcfTTM_up)

	# and float(stock_pd["peTTM"]) > in_peTTM_down \
	# and float(stock_pd["peTTM"]) < in_peTTM_up \
	if float(stock_pd["pbMRQ"]) < in_pbMRQ \
		and float(stock_pd["psTTM"]) < in_psTTM \
		and float(stock_pd["pcfNcfTTM"]) > in_pcfNcfTTM_down \
		and float(stock_pd["pcfNcfTTM"]) < in_pcfNcfTTM_up:
	
		return 1

	else:
		return 0

#卖出时机
def out_time(stock_pd, main_data, stock_code):

	#买入数值设置
	#pbMRQ: x>3.3
	#peTTM: 0 < x < 30
	#psTTM：x>4.2
	#pcfNcfTTM： 0<x <50

	# stock_code = stock_pd["code"].values[0]
	stock_data = main_data[main_data["stock_code"] == stock_code]

	out_pbMRQ = stock_data["out_pbMRQ"].values[0]
	out_psTTM = stock_data["out_psTTM"].values[0]
	out_peTTM_down = stock_data["out_pcfNcfTTM_down"].values[0]
	out_peTTM_up = stock_data["out_pcfNcfTTM_up"].values[0]
	out_pcfNcfTTM_down = stock_data["out_pcfNcfTTM_down"].values[0]
	out_pcfNcfTTM_up = stock_data["out_pcfNcfTTM_up"].values[0]


	# if float(stock_pd["pbMRQ"]) > out_pbMRQ and float(stock_pd["psTTM"]) > out_psTTM:
	if float(stock_pd["pbMRQ"]) < out_pbMRQ and float(stock_pd["psTTM"]) < out_psTTM:
		return 1
	else:
		return 0

#每日行业统计
def industry_analysis(today_data, today_date):

	analysis_agg = {'code':['count'],
	'volume':['mean'],
	'close':['min', 'mean', 'median', 'max'],
	'pctChg':['min', 'mean','median', 'max'],
	'pbMRQ':['min', 'mean','median', 'max'],
	'peTTM':['min', 'mean','median', 'max'],
	'psTTM':['min', 'mean','median', 'max'],
	'pcfNcfTTM':['min', 'mean','median', 'max'],

	}
	# group = today_data.groupby("industry")["close","pctChg"].agg(['min','max','median','mean','count'])
	industry_group_info = today_data.groupby("industry").agg(analysis_agg)

	columns=['industry', 'date','code_count','volume_mean','close_min','close_mean','close_median','close_max','pctChg_min','pctChg_mean','pctChg_median','pctChg_max','pbMRQ_min','pbMRQ_mean','pbMRQ_median','pbMRQ_max','peTTM_min','peTTM_mean','peTTM_median','peTTM_max','psTTM_min','psTTM_mean','psTTM_median','psTTM_max','pcfNcfTTM_min','pcfNcfTTM_mean','pcfNcfTTM_median','pcfNcfTTM_max']

	#行业排序
	industry_volume_sort = industry_group_info['volume']['mean'].sort_values(ascending=False)
	industry_list = industry_volume_sort.index
	# print(group_detail.index)

	industry_volume_item = {}
	for i, industry in enumerate(industry_list):
		industry_volume_item[industry] = i+1

	industry_peTTM_median_sort = industry_group_info['peTTM']['median'].sort_values(ascending=False).index

	industry_peTTM_median_item = {}
	for i, industry in enumerate(industry_peTTM_median_sort):
		industry_peTTM_median_item[industry] = i+1

	# print(industry_peTTM_median_item)



	today_industry_info_pd = pd.DataFrame(columns=columns)

	for industry in industry_list:
		data_list = industry_group_info.loc[industry,].values.tolist()
		data_list.insert(0, industry)
		data_list.insert(1, today_date)
		today_industry_info_pd = today_industry_info_pd.append(pd.Series(data_list, index=columns), ignore_index=True)



	return today_industry_info_pd, industry_peTTM_median_item, industry_volume_item

if __name__ == '__main__':
		# today_stock_info_pd = today_stock_info_pd.reset_index(drop=True)
	# print(type(today_stock_info_pd.loc[0]))

	# today_date = "2020-02-22"
	today_date = str(datetime.datetime.now().date())

	today_stock_info_pd = pd.read_csv("./数据文件/每日股价表/"+today_date+".csv", encoding="gbk")
	# today_stock_info_pd = pf.read_csv("./每日股价表/2020-02-22.csv")

	industry_group_info, industry_peTTM_median_item, industry_volume_item = industry_analysis(today_stock_info_pd, today_date)


	industry_group_info = industry_group_info.set_index("industry")

	# print(industry_group_info)
	# 保存行业数据分析数据
	industry_group_info.to_csv("./数据文件/行业数据分析/每日/"+today_date+".csv", encoding="gbk")

	#分析行业交易量排名
	# industry_volume_sort = industry_group_info["volume_mean"].sort_values(ascending=False).index
	# industry_volume_sort = industry_group_info["volume_mean"].index
	# industry_volume_sort = industry_group_info["industry"].values

	# print(industry_volume_sort)

	# industry_volume_item = {}
	# for i, industry in enumerate(industry_volume_sort):
	# 	industry_volume_item[industry] = i+1

	# print(industry_volume_item)

	#获取行数
	row_count = today_stock_info_pd.shape[0]

	in_stock_pd = pd.DataFrame(columns=['date', 'code', 'industry', 'industry_volume_sort', 'industry_peTTM_median_sort','open', 'high', 'low', 'close', 'preclose',
	 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM',
	 'industry_pbMRQ_mean','industry_pbMRQ_median','industry_peTTM_mean','industry_peTTM_median','industry_psTTM_mean','industry_psTTM_median','industry_pcfNcfTTM_mean','industry_pcfNcfTTM_median'])

	out_stock_pd = pd.DataFrame(columns=['date', 'code', 'industry', 'industry_volume_sort', 'industry_peTTM_median_sort','open', 'high', 'low', 'close', 'preclose',
	 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM',
	 'industry_pbMRQ_mean','industry_pbMRQ_median','industry_peTTM_mean','industry_peTTM_median','industry_psTTM_mean','industry_psTTM_median','industry_pcfNcfTTM_mean','industry_pcfNcfTTM_median'])


	main_data = pd.read_csv("./数据文件/股票关键数据/true.csv", encoding="gbk")
	# main_data = all_stock_code_pd

	#买入时机
	for i in range(0, row_count):

		#如果符合购买条件,则加入购买pd
		# print(today_stock_info_pd.loc[i]["close"])

		in_stock_temp_pd = today_stock_info_pd.loc[i].copy()
		# print("in",type(in_stock_temp_pd))
		stock_code = in_stock_temp_pd["code"]

		
		#判断买入时机
		if in_time(in_stock_temp_pd, main_data, stock_code) == 1:
			stock_industry = main_data[main_data["stock_code"] == stock_code]["stock_industry"].values[0]
			in_stock_temp_pd["industry"] = stock_industry
			in_stock_temp_pd["industry_volume_sort"] = industry_volume_item[stock_industry]
			in_stock_temp_pd["industry_peTTM_median_sort"] = industry_peTTM_median_item[stock_industry]


			in_stock_temp_pd["industry_pbMRQ_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
			in_stock_temp_pd["industry_pbMRQ_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]
			in_stock_temp_pd["industry_peTTM_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
			in_stock_temp_pd["industry_peTTM_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]
			in_stock_temp_pd["industry_psTTM_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
			in_stock_temp_pd["industry_psTTM_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]
			in_stock_temp_pd["industry_pcfNcfTTM_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
			in_stock_temp_pd["industry_pcfNcfTTM_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]
			
			# print(in_stock_temp_pd)
			in_stock_pd = in_stock_pd.append(in_stock_temp_pd, ignore_index=True)
			in_stock_pd.to_csv("./数据文件/建议买入/"+today_date+".csv", index=False, encoding="gbk")
	# print(in_stock_pd)


	#判断卖出时机
	my_stock_pd = pd.read_csv("./数据文件/已买入/stock_code.csv")

	# print(my_stock_pd)

	my_sotck_list = my_stock_pd["stock_code"].values
	# print(my_sotck_list)

	for my_stock in my_sotck_list:

		# print(today_stock_info_pd[today_stock_info_pd["code"] == my_stock])

		out_stock_temp_pd = today_stock_info_pd[today_stock_info_pd["code"] == my_stock].copy()

		# print("out",type(out_stock_temp_pd))
		stock_code = my_stock

		if out_stock_temp_pd.empty == False:
			if out_time(out_stock_temp_pd, main_data, stock_code) == 1:
				stock_industry = main_data[main_data["stock_code"] == stock_code]["stock_industry"].values[0]
				out_stock_temp_pd["industry"] = stock_industry
				out_stock_temp_pd["industry_volume_sort"] = industry_volume_item[stock_industry]
				out_stock_temp_pd["industry_peTTM_median_sort"] = industry_peTTM_median_item[stock_industry]


				out_stock_temp_pd["industry_pbMRQ_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
				out_stock_temp_pd["industry_pbMRQ_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]
				out_stock_temp_pd["industry_peTTM_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
				out_stock_temp_pd["industry_peTTM_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]
				out_stock_temp_pd["industry_psTTM_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
				out_stock_temp_pd["industry_psTTM_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]
				out_stock_temp_pd["industry_pcfNcfTTM_mean"] = industry_group_info["pbMRQ_mean"].loc[stock_industry]
				out_stock_temp_pd["industry_pcfNcfTTM_median"] = industry_group_info["pbMRQ_median"].loc[stock_industry]

				out_stock_temp_pd = out_stock_temp_pd.reindex(columns=['date', 'code', 'industry', 'industry_volume_sort', 'industry_peTTM_median_sort', 'open', 'high', 'low', 'close', 'preclose',
					 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM',
					 'industry_pbMRQ_mean','industry_pbMRQ_median','industry_peTTM_mean','industry_peTTM_median','industry_psTTM_mean','industry_psTTM_median','industry_pcfNcfTTM_mean','industry_pcfNcfTTM_median'])
				out_stock_pd = pd.concat([out_stock_pd,out_stock_temp_pd])

				out_stock_pd.to_csv("./数据文件/建议卖出/"+today_date+".csv", index=False, encoding="gbk")


	if in_stock_pd.empty:
		print("今日无建议买入")

	if out_stock_pd.empty:
		print("今日无建议卖出")




