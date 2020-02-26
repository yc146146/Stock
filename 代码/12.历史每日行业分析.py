import pandas as pd
import datetime
import numpy as np




def main(date):
	today_data = pd.read_csv("./往年每日股价表/"+date+".csv", encoding="gbk")

	# print(today_data.head())


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
	group = today_data.groupby("industry").agg(analysis_agg)

	# print(group.head())

	columns=['industry','date','code_count','volume_mean','close_min','close_mean','close_median','close_max','pctChg_min','pctChg_mean','pctChg_median','pctChg_max','pbMRQ_min','pbMRQ_mean','pbMRQ_median','pbMRQ_max','peTTM_min','peTTM_mean','peTTM_median','peTTM_max','psTTM_min','psTTM_mean','psTTM_median','psTTM_max','pcfNcfTTM_min','pcfNcfTTM_mean','pcfNcfTTM_median','pcfNcfTTM_max']

	#行业排序
	group_detail = group['volume']['mean'].sort_values(ascending=False)
	industry_list = group_detail.index
	# print(group_detail.index)

	today_stock_info_pd = pd.DataFrame(columns=columns)

	for industry in industry_list:
		data_list = group.loc[industry,].values.tolist()
		data_list.insert(0, industry)
		data_list.insert(1, date)
		today_stock_info_pd = today_stock_info_pd.append(pd.Series(data_list, index=columns), ignore_index=True)


	# print(group.iloc[0,].values)

	# print(today_stock_info_pd)

	return today_stock_info_pd

	# group.to_csv("./行业数据分析/历史/"+today_date+".csv", encoding="gbk")

	# group_detail = group['close']['mean']
	# print(group_detail.loc["交通运输"])

	#行业排序
	# group_detail = group['volume']['mean'].sort_values(ascending=False)
	# print(group_detail.index)



if __name__ == '__main__':

	analysis_date_pd = pd.read_csv("./baostock_data/指数/sh.000001_day.csv", encoding="gbk")
	date_list = analysis_date_pd[analysis_date_pd["date"]>"2013-01-01"]["date"].values[0:2]


	# today_date = "2020-02-22"
	# today_date = str(datetime.datetime.now().date())

	for date in date_list:
		today_stock_info_pd = main(date)

		today_stock_info_pd.to_csv("./行业数据分析/历史/"+date+".csv", encoding="gbk", index=False)