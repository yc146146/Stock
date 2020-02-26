import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

#coding:utf-8
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

stock_pd = pd.read_csv("./数据合并处理/sh.600000_day_qfq_c.csv", encoding="gbk")

# print(stock_pd.head())

industry_pd = pd.read_csv("./行业数据分析/历史交易时间线研究/银行.csv", encoding="gbk")


# main = stock_main_pd[["date","close"]].copy()
# main.rename(columns={"close":"stock_main_close"}, inplace=True)
# stock_pd.set_index("date", inplace=True)


# second = stock_pd[["date","industry","close","pbMRQ","peTTM","psTTM","pcfNcfTTM"]].copy()
# second.rename(columns={"close":"stock_second_close"}, inplace=True)
# second.set_index("date", inplace=True)

columns = {"volume_mean":"industry_volume_mean",
"close_mean":"industry_close_mean",
"close_median":"industry_close_median",
"pbMRQ_mean":"industry_pbMRQ_mean",
"pbMRQ_median":"industry_pbMRQ_median",
"peTTM_mean":"industry_peTTM_mean",
"peTTM_median":"industry_peTTM_median",
"psTTM_mean":"industry_psTTM_mean",
"psTTM_median":"industry_psTTM_median",
"pcfNcfTTM_mean":"industry_pcfNcfTTM_mean",
"pcfNcfTTM_median":"industry_pcfNcfTTM_median",
}


industry_pd = industry_pd[["date", "volume_mean", "close_mean", "close_median", 
"pbMRQ_mean","pbMRQ_median", "peTTM_mean","peTTM_median", "psTTM_mean","psTTM_median", "pcfNcfTTM_mean","pcfNcfTTM_median"]]
industry_pd.rename(columns=columns, inplace=True)


merge_date_pd = pd.merge(stock_pd, industry_pd, how="inner", on="date")

print(merge_date_pd.head())

merge_date_pd["industry_volume_mean"] = merge_date_pd["industry_volume_mean"]/100000000
merge_date_pd["stock_main_close"] = merge_date_pd["stock_main_close"]/1000
merge_date_pd["industry_pbMRQ_mean"] = merge_date_pd["industry_pbMRQ_mean"]*10
merge_date_pd["industry_pcfNcfTTM_mean"] = merge_date_pd["industry_pcfNcfTTM_mean"]/10
merge_date_pd["pcfNcfTTM"] = merge_date_pd["pcfNcfTTM"]/10
merge_date_pd["pbMRQ"] = merge_date_pd["pbMRQ"]*10

plt.xlabel("时间")
plt.ylabel("交易量")


# plt.plot(merge_date_pd["date"],merge_date_pd["industry_volume_mean"],color="green",linestyle="-",marker="|", label="industry_volume_mean")  
# plt.plot(merge_date_pd["date"],merge_date_pd["industry_close_mean"],color="red",linestyle="-",marker="|", label="industry_close_mean")  
# plt.plot(merge_date_pd["date"],merge_date_pd["industry_close_median"],color="brown",linestyle="-",marker="|", label="industry_close_median")  
# plt.plot(merge_date_pd["date"],merge_date_pd["industry_pbMRQ_mean"],color="pink",linestyle="-",marker="|", label="industry_pbMRQ_mean")  
# plt.plot(merge_date_pd["date"],merge_date_pd["industry_pbMRQ_median"],color="black",linestyle="-",marker="|", label="industry_pbMRQ_median")  
# plt.plot(merge_date_pd["date"],merge_date_pd["industry_psTTM_mean"],color="black",linestyle="-",marker="|", label="industry_psTTM_mean")  
# plt.plot(merge_date_pd["date"],merge_date_pd["industry_pcfNcfTTM_mean"],color="black",linestyle="-",marker="|", label="industry_pcfNcfTTM_mean")  
plt.plot(merge_date_pd["date"],merge_date_pd["industry_peTTM_mean"],color="black",linestyle="-",marker="|", label="industry_peTTM_mean")  



# plt.plot(merge_date_pd["date"],merge_date_pd["stock_main_close"],color="blue",linestyle="-",marker="|", label="stock_main_close")  
plt.plot(merge_date_pd["date"],merge_date_pd["stock_second_close"],color="orange",linestyle="-",marker="|", label="stock_second_close")  
# plt.plot(merge_date_pd["date"],merge_date_pd["pbMRQ"],color="gray",linestyle="-",marker="|", label="pbMRQ")  
# plt.plot(merge_date_pd["date"],merge_date_pd["psTTM"],color="gray",linestyle="-",marker="|", label="pbMRQ")  
# plt.plot(merge_date_pd["date"],merge_date_pd["pcfNcfTTM"],color="gray",linestyle="-",marker="|", label="pcfNcfTTM")  
plt.plot(merge_date_pd["date"],merge_date_pd["peTTM"],color="gray",linestyle="-",marker="|", label="peTTM_mean")  

#刻度旋转
plt.xticks(rotation=270)

x_major_locator=MultipleLocator(100)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)

plt.legend()
plt.show()