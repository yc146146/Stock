import pandas as pd 
from keras.layers import Dense, Activation, Dropout, SimpleRNN, LSTM, Embedding, Conv1D, Flatten, GlobalMaxPool1D
from keras.models import Sequential, load_model, model_from_json
from keras import optimizers
import keras as K
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt



def fit_data(x_train, y_train, epochs):

	regressor = Sequential()

	regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1], x_train.shape[2])))

	regressor.add(Dropout(0.2))

	regressor.add(LSTM(units = 50, return_sequences = True))

	regressor.add(Dropout(0.2))

	regressor.add(LSTM(units = 50, return_sequences = True))

	regressor.add(Dropout(0.2))

	regressor.add(LSTM(units = 50))

	regressor.add(Dropout(0.2))

	regressor.add(Dense(units = 1))

	regressor.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])

	regressor.fit(x_train, y_train, epochs = epochs, batch_size = 32)
	
	return regressor


def fit_data2(x_train, y_train, epochs):
	model = Sequential()

	# model.add(Dense(256, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(128, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(64, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(32, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(y_train.shape[1]*2, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))

	# model.add(Dense(1, kernel_initializer='random_uniform', bias_initializer='random_uniform'))

	model.add(Dense(units=10))
	model.add(Activation('tanh'))
	# model.add(Dropout(0.5))
	model.add(Dense(units=1))
	model.add(Activation('tanh'))

	# model.add(Dense(y_train.shape[1],input_dim=903, kernel_initializer='random_uniform', bias_initializer='random_uniform'))
	# model.add(Activation('linear'))

	# opt = optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0, amsgrad=False)
	opt = optimizers.SGD(lr=0.3)
	model.compile(optimizer=opt, loss='mean_squared_error', metrics=['accuracy'])

	#训练
	model.fit(x_train, y_train, batch_size=128, epochs=epochs, shuffle=True)

	score = model.evaluate(x_train, y_train, verbose=0)

	print('loss:', score[0], '\t\taccuracy:', score[1])

	# model.save(model_file)

	return model

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

	training_set_x = file_pd[["pbMRQ","peTTM", "psTTM","industry_pbMRQ_mean","industry_peTTM_mean",
	"industry_peTTM_median","industry_psTTM_mean","industry_pbMRQ_mean_sort"]].values
	training_set_y = file_pd[["close"]].values

	# print(len(training_set_y))

	#进行归一化
	sc_x = MinMaxScaler(feature_range = (0, 1))
	sc_y = MinMaxScaler(feature_range = (0, 1))

	print(len(training_set_x))
	print(len(training_set_y))

	x_train = training_set_x[:-100]
	y_train = training_set_y[:-100]

	x_test = training_set_x[-100:]
	y_test = training_set_y[-100:]


	# training_set_scaled_x = sc_x.fit_transform(training_set_x)
	# training_set_scaled_y = sc_y.fit_transform(training_set_y)

	training_set_scaled_x = sc_x.fit_transform(x_train)
	training_set_scaled_y = sc_y.fit_transform(y_train)

	

	y = []

	data_length = len(training_set_y)

	#60数据为1组 1975组
	# for i in range(60, data_length):

	# 	x_train.append(training_set_scaled_x[i-60:i, :])
	# 	y_train.append(training_set_scaled_y[i, 0])

	# 	# X_train.append(training_set[i-60:i, :])
	# 	# y_train.append(training_set[i, 0])
	# 	y.append(training_set_y[i, 0])

	#把 X_train的数据转化到3D维度的数组中，时间步长设置为60，每一步表示一个特征
	x_train, y_train = np.array(training_set_scaled_x), np.array(training_set_scaled_y)

	#shape (1975, 60, 1)
	# x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2]))


	# print(x_train)
	# print("*"*30)
	# print(y_train)

	#训练数据
	models = fit_data2(x_train, y_train, 100)

	# print(y_train.shape)

	testset_scaled_x = sc_x.fit_transform(x_test)

	# predicted_stock_price = models.predict(x_train)
	predicted_stock_price = models.predict(testset_scaled_x)

	# predicted_stock_price = sc_y.inverse_transform(predicted_stock_price)
	predicted_stock_price = sc_y.inverse_transform(predicted_stock_price)



	plt.plot(y_test, color = 'black', label = 'TATA Stock Price')

	plt.plot(predicted_stock_price, color = 'green', label = 'Predicted TATA Stock Price')

	plt.title('TATA Stock Price Prediction')

	plt.xlabel('Time')

	plt.ylabel('TATA Stock Price')

	plt.legend()

	plt.show()





if __name__ == '__main__':
	main()