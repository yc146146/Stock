import pandas as pd 
from keras.layers import Dense, Activation, Dropout, SimpleRNN, LSTM, Embedding, Conv1D, Flatten, GlobalMaxPool1D
from keras.models import Sequential, load_model, model_from_json
from keras import optimizers
import keras as K
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt



def fit_data2(x_train, y_train, epochs):

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

	regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

	regressor.fit(x_train, y_train, epochs = epochs, batch_size = 32, verbose = 2)
	
	return regressor

def fit_data(x_train, y_train, epochs, batch_size):
	regressor = Sequential()
	regressor.add(LSTM(units = 64, activation='relu', return_sequences=False, input_shape=(x_train.shape[1], x_train.shape[2])))
	regressor.add(Dropout(0.2))
	# regressor.add(LSTM(units = 64, activation='tanh', return_sequences = True))
	# regressor.add(Dropout(0.2))
	# regressor.add(LSTM(units = 64, activation='tanh', return_sequences = True))
	# regressor.add(Dropout(0.2))
	# regressor.add(LSTM(units = 64, activation='tanh'))
	# regressor.add(Dropout(0.2))
	# regressor.add(Dense(units = 1, activation="linear"))
	# regressor.add(Dense(y_train.shape[1], activation="linear"))
	regressor.add(Dense(y_train.shape[1]))
	regressor.compile(optimizer='adam', loss='mean_squared_error') 


	regressor.fit(x_train, y_train, epochs = epochs, batch_size = batch_size,verbose = 2, shuffle=False)

	return regressor

#两个思路 
#1.滑动时间窗口预测, x(N,60,8) y(N,8),带入再预测 y(N+1,8)
#2.直接预测后N天数据, x(N,60,8) y(N+1,N+2,N+3,N+4,N+5)

def main():

	stock_code = "sz.002269"
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
	set_x = file_pd[["close", "pbMRQ", "peTTM", "psTTM"]].values
	set_y = file_pd[["close"]].values

	# print(len(training_set_y))

	training_set_x = set_x[:-75]
	training_set_y = set_y[:-75]

	testing_set_x = set_x[-75:]
	testing_set_y = set_y[-75:]

	#进行归一化
	sc_x = MinMaxScaler(feature_range = (0, 1))
	sc_y = MinMaxScaler(feature_range = (0, 1))

	training_set_scaled_x = sc_x.fit_transform(training_set_x)
	training_set_scaled_y = sc_y.fit_transform(training_set_y)

	x_train = []

	y_train = []

	y = []

	y_future = set_y[-15:]

	# print(len(y_future))
	# print(y_future)

	data_length = len(training_set_y) - 15

	#60数据为1组 1975组
	for i in range(60, data_length):

		x_train.append(training_set_scaled_x[i-60:i, :])

		temp_list_y_train = []
		temp_list_y = []
		for j in range(1,16):
			temp_list_y_train.append(training_set_scaled_y[i+j, 0])
			temp_list_y.append(training_set_y[i+j, 0])

		y_train.append(temp_list_y_train)
		# y_train.append([training_set_scaled_y[i+1, 0],training_set_scaled_y[i+2, 0],training_set_scaled_y[i+3, 0],training_set_scaled_y[i+4, 0],training_set_scaled_y[i+5, 0]])

		# X_train.append(training_set[i-60:i, :])
		# y_train.append(training_set[i, 0])
		# y.append([training_set_y[i+1, 0],training_set_y[i+2, 0],training_set_y[i+3, 0],training_set_y[i+4, 0],training_set_y[i+5, 0]])
		y.append(temp_list_y)
	

	#把 X_train的数据转化到3D维度的数组中，时间步长设置为60，每一步表示一个特征
	x_train, y_train = np.array(x_train), np.array(y_train)

	#shape (1975, 60, 1)
	x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2]))

	y = np.array(y)
	y = y.reshape(-1,1)

	# y_future = np.array(y_future).reshape(-1,1)

	# print(y_train.shape)

	#训练数据
	# models = fit_data(x_train, y_train, 50)

	# models = fit_data(x_train, y_train, 300, 32)
	models = fit_data(x_train, y_train, 400, 128)

	# print(y_train.shape)

	# print(len(testing_set_x))
	testing_set_x = testing_set_x.reshape(-1, testing_set_x.shape[1])



	# #这时对于X_test，我们就可以直接使用transform方法。因为此时StandardScaler已经保存了X_train的 \mu 和 \sigma
	testing_set_scaled_x = sc_x.transform(testing_set_x)

	x_test = []
	y_test = testing_set_y[-15:]

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

	#训练
	plt.subplot(2,1,1)
	plt.plot(y, color = 'black', label = 'TATA Stock Price')
	# plt.plot(y_test, color = 'black', label = 'TATA Stock Price')
	plt.plot(predicted_stock_price_train, color = 'green', label = 'Predicted TATA Stock Price')
	plt.title('TATA Stock Price Prediction')
	# plt.xlabel('Time')
	plt.ylabel('TATA Stock Price Train')
	plt.legend()

	#测试
	plt.subplot(2,1,2)
	plt.plot(y_future, color = 'black', label = 'TATA Stock Price')
	# plt.plot(y_test, color = 'black', label = 'TATA Stock Price')
	plt.plot(predicted_stock_price_test, color = 'green', label = 'Predicted TATA Stock Price')
	plt.title('TATA Stock Price Prediction')
	# plt.xlabel('Time')
	plt.ylabel('TATA Stock Price test')
	plt.legend()

	plt.show()





if __name__ == '__main__':
	main()