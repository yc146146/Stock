import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

#coding:utf-8
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


# stock_300106 = pd.read_csv("./baostock_data/sz.399106_m.csv")
# stock_002269 = pd.read_csv("./baostock_data/sz.002269_d.csv")
# stock_000507 = pd.read_csv("./baostock_data/sz.000507_d.csv")

# stock_002269 = pd.read_csv("./res/sz.002269_d.csv")
stock_000507 = pd.read_csv("./res/sz.000507_d.csv")


plt.xlabel("时间")
plt.ylabel("金额")


# plt.plot(stock_002269["date"],stock_002269["close"][4000:],'g-s', label="close")
# plt.plot(stock_002269["date"],stock_002269["round_pbMRQ"],'b-s', label="pbMRQ")  

stock = stock_000507[stock_000507["date"]>"2018-01-01"]



# plt.plot(stock["date"],stock["stock_002269_close"],'r-s', label="stock_002269_close")  
# plt.plot(stock["date"],stock["pbMRQ"],'g-s', label="pbMRQ")  
# # plt.plot(stock_002269["date"][2300:],stock_002269["peTTM/10"][2300:],'y-s', label="peTTM")  
# plt.plot(stock["date"],stock["psTTM"],'b-s', label="psTTM")  
# plt.plot(stock["date"],stock["pcfNcfTTM/100"],color="orange",linestyle="-",marker="|", label="pcfNcfTTM")  

plt.plot(stock["date"],stock["stock_main_close/100"],color="pink",linestyle="-",marker="|", label="stock_main_close")  
plt.plot(stock["date"],stock["stock_second_close"],color="red",linestyle="-",marker="|", label="stock_second_close")  
plt.plot(stock["date"],stock["pbMRQ"],color="green",linestyle="-",marker="|", label="pbMRQ")  
plt.plot(stock["date"],stock["peTTM/10"],color="black",linestyle="-",marker="|", label="peTTM")  
plt.plot(stock["date"],stock["psTTM"],color="blue",linestyle="-",marker="|", label="psTTM")  
plt.plot(stock["date"],stock["pcfNcfTTM/10"],color="orange",linestyle="-",marker="|", label="pcfNcfTTM")  





#刻度旋转
plt.xticks(rotation=270)

x_major_locator=MultipleLocator(100)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)


plt.legend()
plt.show()