import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

#coding:utf-8
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


stock_399106 = pd.read_csv("./baostock_data/sz.399106_m.csv")
stock_002269 = pd.read_csv("./baostock_data/sz.002269_m.csv")
stock_000507 = pd.read_csv("./baostock_data/sz.000507_m.csv")



plt.xlabel("时间")
plt.ylabel("金额")

# print(stock_399106.head())

plt.subplot(311)
plt.plot(stock_399106["date"],stock_399106["open"],'r-s', label="stock_399106") 

#刻度旋转
plt.xticks(rotation=270)

x_major_locator=MultipleLocator(20)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)

plt.subplot(312)
plt.plot(stock_002269["date"],stock_002269["close"],'g-s', label="stock_002269") 

#刻度旋转
plt.xticks(rotation=270)

x_major_locator=MultipleLocator(20)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)

plt.subplot(313)
plt.plot(stock_000507["date"],stock_000507["close"],'b-s',  label="stock_000507") 

#刻度旋转
plt.xticks(rotation=270)

x_major_locator=MultipleLocator(20)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)


plt.legend()
plt.show()