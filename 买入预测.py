import pandas as pd

stock_code = "sz.000507"

stock_pd = pd.read_csv("./res/"+stock_code+"_d.csv")
stock_pd = stock_pd[stock_pd["date"]>"2013-01-01"]

# print(stock_pd)

#买入数值设置
#pbMRQ: 1.79
#peTTM: 0 < x < 30
#psTTM：3.17
#pcfNcfTTM： 0<x <50

in_time = stock_pd[
				(stock_pd["pbMRQ"]<1.79)
				&(stock_pd["psTTM"]<3.17)
				# &(stock_pd["peTTM"]<30)
				# &(stock_pd["peTTM"]>0)
				&(stock_pd["pcfNcfTTM"]>0)
				&(stock_pd["pcfNcfTTM"]<50)
				]

# print(in_time)
in_time.to_csv("./预测结果表/"+stock_code+"_in.csv")


