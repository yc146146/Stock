import pandas as pd
import time
import datetime
import math


#查找日期函数
def find_stock(input_date, stock_date_list):
	for output_date in stock_date_list:
		# if output_date > input_date:
		if output_date.find("-"):
			if time.mktime(time.strptime(output_date,'%Y-%m-%d')) > time.mktime(time.strptime(input_date,'%Y-%m-%d')):
				return output_date
				break
		else:
			if time.mktime(time.strptime(output_date,'%Y/%m/%d')) > time.mktime(time.strptime(input_date,'%Y/%m/%d')):
				return output_date
				break
	return -1

# def find_stock_out(input_date, stock_out_date_list):
# 	for output_date in stock_out_date_list:
# 		if output_date > input_date:
# 			return output_date
# 			break

# res = find_stock(init_in_date, stock_out_date_list)

# print(res)

#制作买入卖出时间字典组
def make_date_item(in_date, stock_date_trade_group_list, stock_in_date_list, stock_out_date_list):
	
	out_date = find_stock(in_date, stock_out_date_list)

	if out_date == -1:
		return -1
	else:
		date_item = {}
		date_item["in"] = in_date
		date_item["out"] = out_date
		stock_date_trade_group_list.append(date_item)

		# print("out_date",out_date)
		in_date_temp = find_stock(out_date, stock_in_date_list)

		# print("in_date_temp",in_date_temp)
		if in_date_temp == -1:
			return -1
		else:
			make_date_item(in_date_temp, stock_date_trade_group_list, stock_in_date_list, stock_out_date_list)


if __name__ == '__main__':

	#股票代码
	# stock_code = "sz.000507"
	# stock_code = "sz.002269"

	all_stock_code_pd = pd.read_csv("./所有股票/baostock_all.csv", encoding="gbk")
	stock_code_list = all_stock_code_pd["code"].values[0:2]

	#投入资金
	init_money = 1000

	for stock_code in stock_code_list:

		stock_in_pd = pd.read_csv("./预测结果表/"+stock_code+"_in.csv")
		stock_out_pd = pd.read_csv("./预测结果表/"+stock_code+"_out.csv")


		# print(stock_in_pd["date"][0])

		stock_in_date_list = stock_in_pd["date"].values 
		stock_out_date_list = stock_out_pd["date"].values 


		# print(stock_in_date_list)
		# print(stock_out_date_list)

		stock_date_trade_group_list = []

		#开始匹配日期
		init_in_date = stock_in_pd["date"][0]
		make_date_item(init_in_date, stock_date_trade_group_list, stock_in_date_list, stock_out_date_list)

		# print(stock_date_trade_group_list)

		profit_file = open("./计算利润分段/"+stock_code+".csv", "w",encoding="gbk")
		profit_file.write("股票代码,买入日期,卖出日期,共计天数,初始金额,实际使用资金,未使用资金,购买股数,买入价格,卖出价格,收益,利润,结余\n")

		#分开计算
		for date_data in stock_date_trade_group_list:
			in_price = stock_in_pd[stock_in_pd["date"]==date_data["in"]]["stock_second_close"].values[0]
			out_price = stock_out_pd[stock_out_pd["date"]==date_data["out"]]["stock_second_close"].values[0]

			if date_data["in"].find("-"):
				in_date = datetime.datetime.strptime(date_data["in"], "%Y-%m-%d")
				out_date = datetime.datetime.strptime(date_data["out"], "%Y-%m-%d")
			else:
				in_date = datetime.datetime.strptime(date_data["in"], "%Y/%m/%d")
				out_date = datetime.datetime.strptime(date_data["out"], "%Y/%m/%d")

			# stock_num = math.floor(init_money/in_price)
			stock_num = ((init_money/in_price)//100)*100

			use_money = stock_num * in_price

			no_use_money = init_money - use_money

			day_num = (out_date - in_date).days

			if stock_num == 0:
				print("购买总数量不得少于100股, 请重新设定金额")
				break

			income_money = stock_num * out_price
			profit_money = income_money - use_money
			total_money = income_money + no_use_money


			# print(in_price)
			# print(out_price)

			profit_file.write("%s,%s,%s,%d,%f,%f,%f,%d,%f,%f,%f,%f,%f\n"%(stock_code,date_data["in"],date_data["out"],day_num,init_money,use_money,no_use_money,stock_num,in_price,out_price,income_money,profit_money,total_money))

			print("date_data",date_data["out"])
			print("共计",total_money)
			print("盈利",profit_money)


		profit_file.close()


