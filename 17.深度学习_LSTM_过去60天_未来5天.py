import pandas as pd 
from keras.layers import Dense, Activation, Dropout, SimpleRNN, LSTM, Embedding, Conv1D, Flatten, GlobalMaxPool1D
from keras.models import Sequential, load_model, model_from_json
from keras import optimizers
import keras as K
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

import winsound


def fit_data2(x_train, y_train, epochs, batch_size):

	regressor = Sequential()

	regressor.add(LSTM(units = 64, return_sequences = True, input_shape = (x_train.shape[1], x_train.shape[2])))
	regressor.add(Dropout(0.2))
	regressor.add(LSTM(units = 64, return_sequences = True))
	regressor.add(Dropout(0.2))
	regressor.add(LSTM(units = 64, return_sequences = True))
	regressor.add(Dropout(0.2))
	regressor.add(LSTM(units = 64))
	regressor.add(Dropout(0.2))
	# regressor.add(Dense(units = 1))
	regressor.add(Dense(y_train.shape[1]))

	regressor.compile(optimizer = "adam", loss = 'mean_squared_error')

	regressor.fit(x_train, y_train, epochs = epochs, batch_size = 32, verbose = 2)
	
	return regressor

def fit_data(x_train, y_train, epochs, batch_size):
	regressor = Sequential()
	regressor.add(LSTM(units = 64, activation='tanh', return_sequences = True, input_shape=(x_train.shape[1], x_train.shape[2])))
	regressor.add(Dropout(0.2))
	regressor.add(LSTM(units = 64, activation='tanh', return_sequences = False))
	regressor.add(Dropout(0.2))
	# regressor.add(LSTM(units = 64, activation='tanh', return_sequences = False))
	# regressor.add(Dropout(0.2))
	# regressor.add(LSTM(units = 64, activation='tanh'))
	# regressor.add(Dropout(0.2))
	
	# regressor.add(Dense(y_train.shape[1], activation="linear"))
	regressor.add(Dense(y_train.shape[1]))

	opt = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

	regressor.compile(optimizer=opt, loss='mean_squared_error') 

	#语音 8、画面 32、自然语言 16
	#遇到某个多信号语音识别任务时 1
	regressor.fit(x_train, y_train, epochs = epochs, batch_size = batch_size,verbose = 2, shuffle=False)
	score = regressor.evaluate(x_train, y_train, batch_size=batch_size, verbose = 2)
	print('loss:', score)

	return regressor

#两个思路 
#1.滑动时间窗口预测, x(N,60,8) y(N,8),带入再预测 y(N+1,8)
#2.直接预测后N天数据, x(N,60,8) y(N+1,N+2,N+3,N+4,N+5)

def main(stock_code, epochs, batch_size):

	# stock_code = "sz.002269"
	# stock_code = "sz.000507"
	file_pd = pd.read_csv("./数据文件/深度学习文件/"+stock_code+".csv", encoding="gbk")

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

	training_set_x = set_x[:-65]
	training_set_y = set_y[:-65]

	testing_set_x = set_x[-65:]
	testing_set_y = set_y[-65:]

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

	#最后5个为预测值,所以 值在最后5个之前的值
	data_length = len(training_set_y) - 5

	# print(len(training_set_scaled_y))

	#60数据为1组 1975组
	for i in range(60, data_length):

		x_train.append(training_set_scaled_x[i-60:i, :])

		y_train.append([training_set_scaled_y[i, 0],training_set_scaled_y[i+1, 0],training_set_scaled_y[i+2, 0],training_set_scaled_y[i+3, 0],training_set_scaled_y[i+4, 0]])

		# X_train.append(training_set[i-60:i, :])
		# y_train.append(training_set[i, 0])
		y.append([training_set_y[i, 0],training_set_y[i+1, 0],training_set_y[i+2, 0],training_set_y[i+3, 0],training_set_y[i+4, 0]])

	

	#把 X_train的数据转化到3D维度的数组中，时间步长设置为60，每一步表示一个特征
	x_train, y_train = np.array(x_train), np.array(y_train)

	#shape (1975, 60, 1)
	x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2]))

	y = np.array(y)
	y = y.reshape(-1,1)

	# y_future = np.array(y_future).reshape(-1,1)

	#batch_128 400 
	#训练数据 60-32-
	# models = fit_data(x_train, y_train, 300, 32) #优
	# models = fit_data(x_train, y_train, 400, 32)
	models = fit_data(x_train, y_train, epochs, batch_size)

	#60-128-
	# models = fit_data(x_train, y_train, 400, 128)
	# models = fit_data(x_train, y_train, 500, 128)
	# models = fit_data(x_train, y_train, 600, 128)
	# models = fit_data(x_train, y_train, 100, 128)
	# models = fit_data(x_train, y_train, epochs, 128)


	#1层 60天
	# models = fit_data(x_train, y_train, 600, 128)
	# models = fit_data(x_train, y_train, 4000, 128)
	# models = fit_data(x_train, y_train, 1, 128)


	# print(testing_set_x.shape)

	# print(len(testing_set_x))
	# testing_set_x = testing_set_x.reshape(-1, 9)
	testing_set_x = testing_set_x.reshape(-1, testing_set_x.shape[1])



	# #这时对于X_test，我们就可以直接使用transform方法。因为此时StandardScaler已经保存了X_train的 \mu 和 \sigma
	testing_set_scaled_x = sc_x.transform(testing_set_x)

	x_test = []
	y_test = testing_set_y[-5:]

	for i in range(60, 61):

		x_test.append(testing_set_scaled_x[i-60:i, :])

	# print(x_test.shape)
	x_test = np.array(x_test)

	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], x_test.shape[2]))

	# print(x_test.shape)

	predicted_stock_price_train = models.predict(x_train)
	predicted_stock_price_test = models.predict(x_test)

	# print(predicted_stock_price_test.shape)


	predicted_stock_price_train = predicted_stock_price_train.reshape(-1,1)
	predicted_stock_price_train = sc_y.inverse_transform(predicted_stock_price_train)

	predicted_stock_price_test = predicted_stock_price_test.reshape(-1,1)
	predicted_stock_price_test = sc_y.inverse_transform(predicted_stock_price_test)

	#保留2位小数
	predicted_stock_price_test = np.around(predicted_stock_price_test, decimals=2)
	# print(predicted_stock_price_test)


	plt.figure()
	#训练
	plt.subplot(2,1,1)
	plt.plot(y, color = 'black', label = 'TATA Stock Price')
	# plt.plot(y_test, color = 'black', label = 'TATA Stock Price')
	plt.plot(predicted_stock_price_train, color = 'green', label = 'Predicted TATA Stock Price')
	plt.title('TATA Stock Price Prediction')
	# plt.xlabel('Time')
	plt.ylabel('TATA Stock Price Train')
	plt.legend()
	plt.grid()

	# print("y_future", y_future)
	# print("predicted_stock_price_test", predicted_stock_price_test)

	#测试
	plt.subplot(2,1,2)
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

	# plt.show()
	plt.savefig("./基于60天预测/"+stock_code+"_60-"+str(batch_size)+"-"+str(epochs)+"-tanh-64-2.png")






if __name__ == '__main__':
	stock_list = ["sz.002269"]
	# epochs_list = [300,400,500,600,800,1000,2000]
	epochs_list = [300,400,500,600,800,1000]
	# epochs_list = [1]

	# stock_list = [
	# "sz.002269",
	# "sz.000507",
	# "sh.600000",
	# "sh.600004",
	# "sh.600006",
	# "sh.600007",
	# "sh.600008",
	# "sz.000001",
	# "sz.000002",
	# "sz.000004",
	# "sz.000005",
	# "sz.000006",
	# ]

	for stock in stock_list:
		for epochs in epochs_list:
			main(stock, epochs, 128)

	winsound.Beep(300,700)