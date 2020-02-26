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

	#### 登陆系统 ####
	lg = bs.login()
	# 显示登陆返回信息
	print('login respond error_code:'+lg.error_code)
	print('login respond  error_msg:'+lg.error_msg)

	today_date = str(datetime.datetime.now().date())
	# today_date = "2020-02-19"

	# index = bs.query_history_k_data_plus("sz.000507",
	#     "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,isST,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM",
	#     start_date=today_date,
	#     end_date=today_date,
	#     frequency="d", adjustflag="3")

	# print(index.fields)

	# stock_code_list = ["sz.000507", "sz.002269"]

	# all_stock_code_pd = pd.read_csv("./股票关键数据/true.csv", encoding="gbk")
	# stock_code_list = all_stock_code_pd["stock_code"].values

	# date_list = ["2013-1-4", "2013-1-7"]

	analysis_date_pd = pd.read_csv("./所有股票/analysis_date.csv", encoding="gbk")
	date_list = analysis_date_pd["date"].values[0:2]

	all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	stock_code_list = all_stock_code_pd["code"].values[0:2]

	print("共有:", len(stock_code_list))

	for date in date_list:
		print("日期:", date)
		today_stock_info_pd = pd.DataFrame(columns=['date', 'code','industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM'])

		count = 0
		for stock_code in stock_code_list:
			print(stock_code)
			industry = all_stock_code_pd[all_stock_code_pd["code"] == stock_code]["industry"].values[0]
			print("第:",count)
			count += 1
			today_stock_info_pd = main(stock_code, date, today_stock_info_pd, industry)

		

		#### 结果集输出到csv文件 ####   
		# print(today_stock_info_pd)
		today_stock_info_pd.to_csv("./往年每日股价表/"+date+".csv", index=False, encoding="gbk")


	#### 登出系统 ####
	bs.logout()




	




