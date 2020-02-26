import baostock as bs
import pandas as pd
import datetime


#单日股价获取函数
def main(stock_code, date, today_stock_info_pd, industry):
	#### 获取沪深A股历史K线数据 ####
	# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
	# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
	rs = bs.query_history_k_data_plus(stock_code,
	    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,isST,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM",
	    start_date=date,
	    end_date=date,
	    frequency="d", adjustflag="3")
	# print('query_history_k_data_plus respond error_code:'+rs.error_code)
	# print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

	# rs = bs.query_history_k_data_plus(stock_code,
 #    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,isST,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM",
 #    start_date="2020-02-21",
 #    end_date="2020-02-21",
 #    frequency="d", adjustflag="3")
	# print('query_history_k_data_plus respond error_code:'+rs.error_code)
	# print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)



	#### 打印结果集 ####
	data_list = []
	while (rs.error_code == '0') & rs.next():
		# 获取一条记录，将记录合并在一起
		data_list.append(rs.get_row_data())

	
	columns=['date', 'code', 'industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM']

	# print(data_list[0])
	# today_data = data_list[0]
	# print(data_list[0])
	
	# print(data_list[0])

	if data_list:
		#插入行业标识
		data_list[0].insert(2, industry)

		#追加
		today_stock_info_pd = today_stock_info_pd.append(pd.DataFrame(data_list, columns=columns), ignore_index=True)


	# today_stock_info_pd[today_stock_info_pd["code"==stock_code]]["industry"] = industry
	# today_stock_info_pd = today_stock_info_pd.reindex(columns=['date', 'code', 'industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM'])

	return today_stock_info_pd


if __name__ == '__main__':


	# analysis_date_pd = pd.read_csv("./所有股票/analysis_date.csv", encoding="gbk")
	# date_list = analysis_date_pd["date"].values[0:2]

	analysis_date_pd = pd.read_csv("./baostock_data/指数/sh.000001_day.csv", encoding="gbk")
	date_list = analysis_date_pd[analysis_date_pd["date"]>"2013-01-01"]["date"].values



	all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	all_stock_code_list = all_stock_code_pd["code"].values

	# print(date_list)

	# print(stock_code_pd.head())
	# print(stock_code_pd[stock_code_pd["date"]=="1999-11-10"])
	# print(type(stock_code_pd[stock_code_pd["date"]=="1999-11-10"]))

	# print("共有:", len(stock_code_list))

	columns=['date', 'code','industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM']
	for date in date_list:
		print("日期:", date)
		today_stock_info_pd = pd.DataFrame(columns=columns)

		
		count = 0
		for stock_code in all_stock_code_list:

			print(stock_code)
			print("第:",count)
			count += 1

			stock_code_pd = pd.read_csv("./baostock_data/股票/"+stock_code+"_day_qfq.csv", encoding="gbk")

			# print(stock_code_pd)

			temp_pd = stock_code_pd[stock_code_pd["date"]==date]

			#判断临时表是否为空
			if temp_pd.empty == False:
				# print(temp_pd)
				today_stock_info_pd = today_stock_info_pd.append(pd.DataFrame(temp_pd, columns=columns), ignore_index=True)

				# today_stock_info_pd = main(stock_code, date, today_stock_info_pd, industry)

		

		#### 结果集输出到csv文件 ####   
		# print(today_stock_info_pd)
		today_stock_info_pd.to_csv("./往年每日股价表/"+date+".csv", index=False, encoding="gbk")





	




