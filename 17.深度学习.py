import pandas as pd 
from keras.layers import Dense, Activation, Dropout, SimpleRNN, LSTM, Embedding, Conv1D, Flatten, GlobalMaxPool1D
from keras.models import Sequential, load_model, model_from_json
from keras import optimizers
import keras as K
import numpy as np
import os



def fit_data(x_train, y_train):
	model = Sequential()

	# model.add(Dense(256, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(128, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(64, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(32, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))
	# model.add(Dense(y_train.shape[1]*2, activation="relu", kernel_initializer='random_uniform', bias_initializer='random_uniform' ))

	# model.add(Dense(1, kernel_initializer='random_uniform', bias_initializer='random_uniform'))

	model.add(Dense(units=10))
	model.add(Activation('tanh'))
	model.add(Dense(units=1))
	model.add(Activation('tanh'))

	# model.add(Dense(y_train.shape[1],input_dim=903, kernel_initializer='random_uniform', bias_initializer='random_uniform'))
	# model.add(Activation('linear'))

	# opt = optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0, amsgrad=False)
	opt = optimizers.SGD(lr=0.3)
	model.compile(optimizer=opt, loss='mean_squared_error', metrics=['accuracy'])

	#训练
	model.fit(x_train, y_train, batch_size=128, epochs=1000, shuffle=True)

	score = model.evaluate(x_train, y_train, verbose=0)

	print('loss:', score[0], '\t\taccuracy:', score[1])

	# model.save(model_file)

def main():

	stock_code = "sz.002269"
	file_pd = pd.read_csv("./数据文件/深度学习文件/"+stock_code+".csv", encoding="gbk")

	# print(file_pd.head())

	x_pd = file_pd.drop(["date","code","industry","close"], axis=1)

	# print(x_pd.head())

	y_pd = file_pd["close"]

	# print(y_pd.head())

	x_train = x_pd.values

	y_train = y_pd.values

	#训练数据
	fit_data(x_train, y_train)

	# print(y_train.shape)






if __name__ == '__main__':
	main()