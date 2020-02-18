import tushare as ts

# ts.set_token('65bf011ea83b359915032eb0c44b1793b033beb4c4c4ab1e37f36752')


# pro = ts.pro_api()

# # df = pro.daily(ts_code='000001.SZ', start_date='20150701', end_date='20150718')

# # print(df)

# # df = pro.adj_factor(ts_code='000001.SZ', trade_date='')

# df = ts.get_h_data('000001.SZ', start='2019-01-01', end='2019-03-16')

# print(df)


# r = ShowapiRequest("http://route.showapi.com/1529-2","my_appId","my_appSecret" )
# r.addBodyPara("begin", "2016-09-01")
# r.addBodyPara("end", "2016-09-02")
# r.addBodyPara("code", "600004")
# res = r.post()
# print(res.text) # 返回信息



# df = ts.get_stock_basics()
# date = df.ix['600848']
# a = ts.get_h_data('399106', index=True)

# df = ts.get_tick_data('600848',date='2018-12-12',src='tt')
# df.head(10)

# print(a)


stock_code = "000507.SZ"

# pro = ts.pro_api()
# df = pro.daily(ts_code=stock_code,  end_date='2020201')
# df = pro.index_daily(ts_code=stock_code, end_date='2020201')

#获取前复权信息
# df = ts.pro_bar(ts_code=stock_code, adj="qfq", start_date='1960-01-01', end_date='2020-02-01')


df = ts.get_industry_classified()

print(df)
df.to_csv("./行业/all.csv",encoding="gbk", index=False)