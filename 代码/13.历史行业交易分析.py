import pandas as pd
import datetime
import numpy as np




def main(date, industry_date_pd, industry):

	industry_info_pd = pd.read_csv("./行业数据分析/历史/"+date+".csv", encoding="gbk")
	industry_info_pd.set_index("industry", inplace=True, drop=False)

	# print(industry_info_pd.head())

	# print(industry_info_pd.loc["银行"])

	# print(industry)
	data_list = industry_info_pd.loc[industry]

	# print(data_list)

	industry_date_pd = industry_date_pd.append(data_list, ignore_index=True)

	# print(industry_date_pd)

	return industry_date_pd

	# analysis_agg = {'code':['count'],
	# 'volume':['mean'],
	# 'close':['min', 'mean', 'median', 'max'],
	# 'pctChg':['min', 'mean','median', 'max'],
	# 'pbMRQ':['min', 'mean','median', 'max'],
	# 'peTTM':['min', 'mean','median', 'max'],
	# 'psTTM':['min', 'mean','median', 'max'],
	# 'pcfNcfTTM':['min', 'mean','median', 'max'],

	# }
	# # group = today_data.groupby("industry")["close","pctChg"].agg(['min','max','median','mean','count'])
	# group = today_data.groupby("industry").agg(analysis_agg)

	# # print(group.head())

	# columns=['industry','date','code_count','volume_mean','close_min','close_mean','close_median','close_max','pctChg_min','pctChg_mean','pctChg_median','pctChg_max','pbMRQ_min','pbMRQ_mean','pbMRQ_median','pbMRQ_max','peTTM_min','peTTM_mean','peTTM_median','peTTM_max','psTTM_min','psTTM_mean','psTTM_median','psTTM_max','pcfNcfTTM_min','pcfNcfTTM_mean','pcfNcfTTM_median','pcfNcfTTM_max']

	# #行业排序
	# # group_detail = group['volume']['mean'].sort_values(ascending=False)
	# group_detail = group['volume']['mean'].sort_values(ascending=False)
	# industry_list = group_detail.index
	# # print(group_detail.index)

	# today_stock_info_pd = pd.DataFrame(columns=columns)

	# for industry in industry_list:
	# 	data_list = group.loc[industry,].values.tolist()
	# 	data_list.insert(0, industry)
	# 	data_list.insert(1, date)
	# 	today_stock_info_pd = today_stock_info_pd.append(pd.Series(data_list, index=columns), ignore_index=True)


	# print(group.iloc[0,].values)

	# print(today_stock_info_pd)

	# return today_stock_info_pd

	# group.to_csv("./行业数据分析/历史/"+today_date+".csv", encoding="gbk")

	# group_detail = group['close']['mean']
	# print(group_detail.loc["交通运输"])

	#行业排序
	# group_detail = group['volume']['mean'].sort_values(ascending=False)
	# print(group_detail.index)



if __name__ == '__main__':

	analysis_date_pd = pd.read_csv("./baostock_data/指数/sh.000001_day.csv", encoding="gbk")
	date_list = analysis_date_pd[analysis_date_pd["date"]>"2013-01-01"]["date"].values

	industry_list = [
			"银行",
			"钢铁",
			"非银金融",
			"建筑装饰",
			"房地产",
			"采掘",
			"有色金属",
			"交通运输",
			"建筑材料",
			"综合",
			"食品饮料",
			"公用事业",
			"农林牧渔",
			"商业贸易",
			"机械设备",
			"轻工制造",
			"国防军工",
			"通信",
			"电子",
			"家用电器",
			"汽车",
			"化工",
			"电气设备",
			"传媒",
			"医药生物",
			"纺织服装",
			"计算机",
			"休闲服务"
			]

	# industry_list = [
	# 		"银行",
	# 		]

	list_len = len(industry_list)
	count_num = 0

	columns=['date','industry','code_count','volume_mean','close_min','close_mean','close_median','close_max','pctChg_min','pctChg_mean','pctChg_median','pctChg_max','pbMRQ_min','pbMRQ_mean','pbMRQ_median','pbMRQ_max','peTTM_min','peTTM_mean','peTTM_median','peTTM_max','psTTM_min','psTTM_mean','psTTM_median','psTTM_max','pcfNcfTTM_min','pcfNcfTTM_mean','pcfNcfTTM_median','pcfNcfTTM_max']
	for industry in industry_list:
		print(industry)
		industry_date_pd = pd.DataFrame()
		for date in date_list:
			print(str(count_num)+" / "+str(list_len))
			count_num += 1

			industry_date_pd = main(date, industry_date_pd, industry)

		industry_date_pd = industry_date_pd.reindex(columns=columns)

		industry_date_pd.to_csv("./行业数据分析/历史交易时间线研究/"+industry+".csv", encoding="gbk", index=False)
		# print(industry_date_pd)