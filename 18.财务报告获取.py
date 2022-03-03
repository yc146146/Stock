import baostock as bs
import pandas as pd

start_date = 1990
end_date = 2021

def find_data(code, year_list, quarter_list):
	# 查询季频估值指标盈利能力
	profit_list = []

	for  year in year_list:
		for quarter in quarter_list:
			rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
			while (rs_profit.error_code == '0') & rs_profit.next():
				profit_list.append(rs_profit.get_row_data())



	result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)

	# print(result_profit)
	return result_profit


def main():
	# 登陆系统
	lg = bs.login()
	# 显示登陆返回信息
	print('login respond error_code:'+lg.error_code)
	print('login respond  error_msg:'+lg.error_msg)


	all_stock_code_pd = pd.read_csv("./数据文件/所有股票/deep_learning_code.csv", encoding="gbk")
	code_list = all_stock_code_pd["code"].values[:2]

	# print(code_list)

	# code_list = ["sz.002624"] 
	# year_list = ["2016","2017","2018","2019","2020"] 
	# year_list = ["2017","2018","2019","2020"] 

	year_list = []
	for year in range(start_date, end_date):
		year_list.append(year)

	quarter_list = ["1","2","3","4"] 
	# quarter_list = ["3","4"] 

	for code in code_list:
		result_profit = find_data(code, year_list, quarter_list)

		result_profit["year"] = result_profit["statDate"].str[0:4]
		result_profit["quarter"] = result_profit["statDate"].str[5:7]

		result_profit["quarter"].replace("03", 2, inplace=True)
		result_profit["quarter"].replace("06", 3, inplace=True)
		result_profit["quarter"].replace("09", 4, inplace=True)
		result_profit["quarter"].replace("12", 12, inplace=True)

		# 打印输出
		# print(result_profit)
		# 结果集输出到csv文件
		result_profit.to_csv("./数据文件/股票财报表/"+code+".csv", encoding="gbk", index=False)



	# 登出系统
	bs.logout()


if __name__ == '__main__':
	main()

	




