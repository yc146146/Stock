import baostock as bs
import pandas as pd
import datetime

import multiprocessing

#单日股价获取函数
def main(task_id, date_list, all_stock_code_list):

	print("task_id", task_id)
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
		today_stock_info_pd.to_csv("./往年每日股价表_2/"+date+".csv", index=False, encoding="gbk")

if __name__ == '__main__':


	# analysis_date_pd = pd.read_csv("./所有股票/analysis_date.csv", encoding="gbk")
	# date_list = analysis_date_pd["date"].values[0:2]

	analysis_date_pd = pd.read_csv("./baostock_data/指数/sh.000001_day.csv", encoding="gbk")
	date_list = analysis_date_pd[analysis_date_pd["date"]>"2019-01-01"]["date"].values[11:]

	# print(date_list)

	all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	all_stock_code_list = all_stock_code_pd["code"].values

	# print(date_list)

	# print(stock_code_pd.head())
	# print(stock_code_pd[stock_code_pd["date"]=="1999-11-10"])
	# print(type(stock_code_pd[stock_code_pd["date"]=="1999-11-10"]))

	# print("共有:", len(stock_code_list))

	# a = [1,2,3,4,5,6,7,8,9,10,11]
	#开启进程数
	group = 10

	total_num = len(date_list)

	group_num = total_num // group

	last_num = total_num - group_num * (group-1)

	

	# for i in range(0,(group-1)):
	# 	date_list_in_temp = date_list[i*group_num:(i+1)*group_num]
	# 	print(date_list_in_temp)

	# date_list_out_temp = date_list[(group-1)*group_num:total_num]
	# print(date_list_out_temp)

	process_list = []
	for i in range(0,(group-1)):
		date_list_in_temp = date_list[i*group_num:(i+1)*group_num]
		process_temp = multiprocessing.Process(target=main, args=("task_"+ str(i), date_list_in_temp, all_stock_code_list))
		process_list.append(process_temp)
		process_temp.start()

	date_list_out_temp = date_list[(group-1)*group_num:total_num]
	process_temp = multiprocessing.Process(target=main, args=("task_last", date_list_out_temp, all_stock_code_list))
	process_list.append(process_temp)
	process_temp.start()

	for process in process_list:
		process.join()  #等待子线程全部执行完		

	print("分析完成")





	




