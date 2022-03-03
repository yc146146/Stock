import pandas as pd 
from keras.layers import Dense, Activation, Dropout, SimpleRNN, LSTM, Embedding, Conv1D, Flatten, GlobalMaxPool1D
from keras.models import Sequential, load_model, model_from_json
from keras import optimizers
import keras as K
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt



#两个思路 
#1.滑动时间窗口预测, x(N,60,8) y(N,8),带入再预测 y(N+1,8)
#2.直接预测后N天数据, x(N,60,8) y(N+1,N+2,N+3,N+4,N+5)

def main():

	stock_code = "sz.002269"
	# stock_code = "sz.000507"
	file_pd = pd.read_csv("./数据文件/深度学习预测文件/"+stock_code+"_day_qfq.csv", encoding="gbk")
	# file_pd = pd.read_csv("./数据文件/深度学习文件/"+stock_code+".csv", encoding="gbk")


	# print(file_pd.head())

	# x_pd = file_pd.drop(["date","code","industry","close"], axis=1)
	# x_pd = file_pd[["close"]]

	# print(x_pd.head())

	# y_pd = file_pd["close"]

	# print(y_pd.head())
	# x_train = x_pd.values
	#y_train = y_pd.values

	# set_x = file_pd[["close","pbMRQ","peTTM", "psTTM","industry_pbMRQ_mean","industry_peTTM_mean",
	# "industry_peTTM_median","industry_psTTM_mean","industry_pbMRQ_mean_sort"]].values

	# set_x = file_pd[["close", "pbMRQ", "peTTM", "psTTM","industry_pbMRQ_mean_sort"]].values
	# set_x = file_pd[["close", "pbMRQ", "peTTM", "psTTM"]].values
	set_x = file_pd[["close", "pbMRQ", "peTTM", "psTTM","pcfNcfTTM"]].values
	set_y = file_pd[["close"]].values

	# print(len(training_set_y))

	training_set_x = set_x[:-35]
	training_set_y = set_y[:-35]

	testing_set_x = set_x[-35:]
	testing_set_y = set_y[-35:]

	future_set_x = set_x[-30:]


	#进行归一化
	sc_x = MinMaxScaler(feature_range = (0, 1))
	sc_y = MinMaxScaler(feature_range = (0, 1))

	training_set_scaled_x = sc_x.fit_transform(training_set_x)
	training_set_scaled_y = sc_y.fit_transform(training_set_y)


	x_train = []

	y_train = []

	y = []
	# y_future = [training_set_y[-5],training_set_y[-4],training_set_y[-3],training_set_y[-2],training_set_y[-1]]
	y_future = set_y[-5:]
	# print(y_future)


	#1层 30天
	# models = fit_data(x_train, y_train, 400, 128)

	models = load_model("./深度学习模型/model_"+stock_code+"_30_1层.h5")

	# score = models.evaluate(x_train, y_train, verbose=1, batch_size=128)
	# print('loss:', score)




	# print(testing_set_x.shape)

	# print(len(testing_set_x))
	# testing_set_x = testing_set_x.reshape(-1, 9)
	testing_set_x = testing_set_x.reshape(-1, testing_set_x.shape[1])
	future_set_x = future_set_x.reshape(-1, future_set_x.shape[1])




	# #这时对于X_test，我们就可以直接使用transform方法。因为此时StandardScaler已经保存了X_train的 \mu 和 \sigma
	testing_set_scaled_x = sc_x.transform(testing_set_x)
	future_set_scaled_x = sc_x.transform(future_set_x)


	x_test = []
	y_test = testing_set_y[-5:]

	x_test = [testing_set_scaled_x[0:30, :]]
	x_future = [future_set_scaled_x]


	# for i in range(30, 31):
	# 	x_test.append(testing_set_scaled_x[i-30:i, :])

	# print(x_test.shape)
	x_test = np.array(x_test)
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], x_test.shape[2]))

	x_future = np.array(x_future)
	x_future = np.reshape(x_future, (x_future.shape[0], x_future.shape[1], x_future.shape[2]))

	# print(x_test.shape)

	predicted_stock_price_test = models.predict(x_test)
	predicted_stock_price_future = models.predict(x_future)



	predicted_stock_price_test = predicted_stock_price_test.reshape(-1,1)
	predicted_stock_price_test = sc_y.inverse_transform(predicted_stock_price_test)

	#保留2位小数
	predicted_stock_price_test = np.around(predicted_stock_price_test, decimals=2)


	predicted_stock_price_future = predicted_stock_price_future.reshape(-1,1)
	predicted_stock_price_future = sc_y.inverse_transform(predicted_stock_price_future)

	#保留2位小数
	predicted_stock_price_future = np.around(predicted_stock_price_future, decimals=2)



	#测试
	plt.subplot(2,1,1)
	plt.plot(y_future, color = 'black', label = 'TATA Stock Price')
	# plt.plot(y_test, color = 'black', label = 'TATA Stock Price')
	plt.plot(predicted_stock_price_test, color = 'green', label = 'Predicted TATA Stock Price')
	#把y轴的刻度间隔设置为10，并存在变量里
	# y_major_locator = plt.MultipleLocator(0.1)
	# #ax为两条坐标轴的实例
	# ax=plt.gca()
	# ax.yaxis.set_major_locator(y_major_locator)
	# plt.ylim(-5,110)
	
	plt.title('TATA Stock Price Prediction')
	# plt.xlabel('Time')
	plt.ylabel('TATA Stock Price test')
	plt.legend()
	plt.grid()

	plt.subplot(2,1,2)
	plt.plot(predicted_stock_price_future, color = 'green', label = 'Predicted TATA Stock Price')
	#把y轴的刻度间隔设置为10，并存在变量里
	# y_major_locator = plt.MultipleLocator(0.1)
	# #ax为两条坐标轴的实例
	# ax=plt.gca()
	# ax.yaxis.set_major_locator(y_major_locator)
	# plt.ylim(-5,110)
	
	plt.title('TATA Stock Price Prediction')
	# plt.xlabel('Time')
	plt.ylabel('TATA Stock Price test')
	plt.legend()
	plt.grid()

	plt.show()





if __name__ == '__main__':
	main()