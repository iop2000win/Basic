# LSTM modeling Basic

import os
import sys

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
# matplotlib option setting
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.unicode_minus'] = False

# ML related library
import sklearn as sc
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error, r2_score

X = []
y = []

X_data = []
y_data = []
window_size = 10 # 시계열 설정 사이즈

for i in range(len(y) - window_size):
	_x = X[i:i+window_size]
	_y = y[i+window_size]

	X_data.append(_x)
	y_data.append(_y)

# train, test 구분. validation set 구분도 해주면 좋다.
X_train, X_test, y_train, y_test = train_test_split(X_data, 			# data feature 정보
													y_data,				# data label
													test_size = 0.3,	# train set 과 test set 비율 설정
													shuffle = False,	# train set, test set을 나눌 때 데이터 추출에 랜덤성을 둘 것인지 결정,
																		# 시계열 데이터의 경우 데이터 순서가 결과에 영향을 미치므로 shuffle해서는 안된다.
													random_state = 23	# 모델 테스트 과정에서의 데이터 일관성을 위해 설정
													)

print(f'X_train.shape: {X_train.shape}')
print(f'y_train.shape: {y_train.shape}')
print(f'X_test.shape: {X_test.shape}')
print(f'y_test.shape: {y_test.shape}')


# modeling based on Keras
model = Sequential()

model.add(LSTM(units = 10,
			   activation = 'relu',
			   return_sequences = True,
			   input_shape = (window_size, 5)
			   )
			)
model.add(Dropout(0.1))
model.add(LSTM(units = 10,
			   activation = 'relu'
			   )
			)
model.add(Dropout(0.1))
model.add(Dense(units = 1))

model.summary()


# learning activation
model.compile(optimizer = 'adam',
			  loss = 'mean_squared_error')

model.fit(X_train,
		  y_train,
		  epochs = 60,
		  batch_size = 30,
		  verbose = 0 # (0, 1, 2) 학습 진행 정도를 표시
		  )


# test set에 대한 예측 결과 반환
y_pred = model.predict(X_test)


# test set에 대한 예측 결과와 실제 test set 값을 비교하여 결과를 시각화하여 표현



# 예측 성능 지표를 통한 결과 분석

MAE = mean_absolute_error(y_test, y_pred)
RMSE = np.sqrt(mean_squared_error(y_test, y_pred))
MSLE = mean_squared_log_error(y_test, y_pred)
RMSLE = np.sqrt(mean_squared_log_error(y_test, y_pred))
R2 = r2_score(y_test, y_pred)