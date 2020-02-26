import baostock as bs
import pandas as pd
import datetime


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

	# in_time = stock_pd[
	# 				(stock_pd["pbMRQ"] < in_pbMRQ)
	# 				&(stock_pd["psTTM"] < in_psTTM)
	# 				# &(stock_pd["peTTM"]>in_peTTM_down)
	# 				# &(stock_pd["peTTM"]<in_peTTM_up)
	# 				&(stock_pd["pcfNcfTTM"] > in_pcfNcfTTM_down)
	# 				&(stock_pd["pcfNcfTTM"] < in_pcfNcfTTM_up)
	# 				]

	# print(in_time)

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


	if float(stock_pd["pbMRQ"]) > out_pbMRQ and float(stock_pd["psTTM"]) > out_psTTM:
		return 1
	else:
		return 0



#单日股价获取函数
def main(stock_code, today_date, today_stock_info_pd, industry):
	#### 获取沪深A股历史K线数据 ####
	# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
	# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
	# rs = bs.query_history_k_data_plus(stock_code,
	#     "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,isST,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM",
	#     start_date=today_date,
	#     end_date=today_date,
	#     frequency="d", adjustflag="3")
	# print('query_history_k_data_plus respond error_code:'+rs.error_code)
	# print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

	rs = bs.query_history_k_data_plus(stock_code,
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,isST,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM",
    start_date="2020-02-21",
    end_date="2020-02-21",
    frequency="d", adjustflag="3")
	print('query_history_k_data_plus respond error_code:'+rs.error_code)
	print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)



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
	today_stock_info_pd = pd.DataFrame(columns=['date', 'code','industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM'])

	# stock_code_list = ["sz.000507", "sz.002269"]

	all_stock_code_pd = pd.read_csv("./股票关键数据/true.csv", encoding="gbk")
	stock_code_list = all_stock_code_pd["stock_code"].values

	print("共有:", len(stock_code_list))
	count = 0
	for stock_code in stock_code_list:
		print(stock_code)
		industry = all_stock_code_pd[all_stock_code_pd["stock_code"] == stock_code]["stock_industry"].values[0]
		print("第:",count)
		count += 1
		today_stock_info_pd = main(stock_code, today_date, today_stock_info_pd, industry)

	#### 登出系统 ####
	bs.logout()

	#### 结果集输出到csv文件 ####   
	print(today_stock_info_pd)
	today_stock_info_pd.to_csv("./每日股价表/"+today_date+".csv", index=False, encoding="gbk")



	# today_stock_info_pd = today_stock_info_pd.reset_index(drop=True)
	# print(type(today_stock_info_pd.loc[0]))

	#获取行数
	row_count = today_stock_info_pd.shape[0]

	in_stock_pd = pd.DataFrame(columns=['date', 'code', 'industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM'])
	out_stock_pd = pd.DataFrame(columns=['date', 'code', 'industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM'])


	# main_data = pd.read_csv("./股票关键数据/true.csv", encoding="gbk")
	main_data = all_stock_code_pd

	#买入时机
	for i in range(0, row_count):

		#如果符合购买条件,则加入购买pd
		# print(today_stock_info_pd.loc[i]["close"])

		in_stock_temp_pd = today_stock_info_pd.loc[i]
		# print("in",type(in_stock_temp_pd))
		stock_code = in_stock_temp_pd["code"]

		#判断买入时机
		if in_time(in_stock_temp_pd, main_data, stock_code) == 1:
			in_stock_temp_pd["industry"] = main_data[main_data["stock_code"] == stock_code]["stock_industry"].values[0]
			# print(in_stock_temp_pd)
			in_stock_pd = in_stock_pd.append(in_stock_temp_pd, ignore_index=True)
			in_stock_pd.to_csv("./建议买入/"+today_date+".csv", index=False, encoding="gbk")
	# print(in_stock_pd)


	#判断卖出时机
	my_stock_pd = pd.read_csv("./已买入/stock_code.csv")

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
				out_stock_temp_pd["industry"] = main_data[main_data["stock_code"] == stock_code]["stock_industry"].values[0]
				# out_stock_pd = out_stock_pd.append(out_stock_temp_pd, ignore_index=True)
				out_stock_temp_pd = out_stock_temp_pd.reindex(columns=['date', 'code', 'industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM'])
				out_stock_pd = pd.concat([out_stock_pd,out_stock_temp_pd])

				out_stock_pd.to_csv("./建议卖出/"+today_date+".csv", index=False, encoding="gbk")


	if in_stock_pd.empty:
		print("今日无建议买入")

	if out_stock_pd.empty:
		print("今日无建议卖出")





	




