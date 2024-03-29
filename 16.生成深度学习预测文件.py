import baostock as bs
import pandas as pd



def main(stock_code, end_date):


	#### 获取沪深A股历史K线数据 ####
	# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
	# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
	# adjustflag：复权类型，
	# 默认不复权：3
	# 1：后复权
	# 2：前复权。
	# 已支持分钟线、日线、周线、月线前后复权。
	
	rs = bs.query_history_k_data_plus(stock_code,
	    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,isST,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM",
	    start_date='1960-01-01',
	    end_date=end_date,
	    frequency="d", adjustflag="2")

	#### 打印结果集 ####
	data_list = []
	while (rs.error_code == '0') & rs.next():
	    # 获取一条记录，将记录合并在一起
	    data_list.append(rs.get_row_data())
	result = pd.DataFrame(data_list, columns=rs.fields)

	#插入行业信息
	# result["industry"] = industry
	#重新设定行索引
	# result = result.reindex(columns=['date', 'code', 'industry', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'isST', 'pctChg', 'pbMRQ', 'peTTM', 'psTTM', 'pcfNcfTTM'])

	#### 结果集输出到csv文件 ####   
	result.to_csv("./数据文件/深度学习预测文件/"+stock_code+"_day_qfq.csv", index=False, encoding="gbk")
	# print(result)



if __name__ == '__main__':


	# all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	# all_stock_code_list = all_stock_code_pd["code"].values


	all_stock_code_list = ["sz.002269"]
	# all_stock_code_list = ["sz.000507"]
	
	end_date='2020-03-17'

	# print(all_stock_code_list)

	#### 登陆系统 ####
	lg = bs.login()
	# 显示登陆返回信息
	print('login respond error_code:'+lg.error_code)
	print('login respond  error_msg:'+lg.error_msg)


	print("共有:", len(all_stock_code_list))
	count = 0

	# all_stock_code_list = ["sh.600074", "sh.600119"]
	for stock_code in all_stock_code_list:
		print("第:",count)
		count += 1
		# industry = all_stock_code_pd[all_stock_code_pd["code"] == stock_code]["industry"].values[0]
		# main(stock_code, industry)
		main(stock_code, end_date)



	#### 登出系统 ####
	bs.logout()