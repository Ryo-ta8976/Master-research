from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# CSVファイルの読み込み
df1 = pd.read_csv('../data_2014-2015.csv')
df2 = pd.read_csv('../data_2015-2016.csv')
df3 = pd.read_csv('../data_2016-2017.csv')
df4 = pd.read_csv('../data_2017-2018.csv')
df5 = pd.read_csv('../data_2018-2019.csv')


# 欠損値の穴埋め
df1 = df1.fillna(method='ffill')
df2 = df2.fillna(method='ffill')
df3 = df3.fillna(method='ffill')
df4 = df4.fillna(method='ffill')
df5 = df5.fillna(method='ffill')

# yearの削除
df1 = df1.loc[:, ['month', 'day', 'snow']]
df2 = df2.loc[:, ['month', 'day', 'snow']]
df3 = df3.loc[:, ['month', 'day', 'snow']]
df4 = df4.loc[:, ['month', 'day', 'snow']]
df5 = df5.loc[:, ['month', 'day', 'snow']]

# データの標準化
scaler = MinMaxScaler(feature_range=(0, 1))
dataset1 = scaler.fit_transform(df1)
dataset2 = scaler.fit_transform(df2)
dataset3 = scaler.fit_transform(df3)
dataset4 = scaler.fit_transform(df4)
dataset5 = scaler.fit_transform(df5)
# dataset1=df1
# dataset2=df2
# dataset3=df3
# dataset4=df4
# dataset5=df5


# データの整形
def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        xset = []
        for j in range(dataset.shape[1]):
            xset.append(dataset[i:i+look_back, j])
        dataY.append(dataset[i+look_back, 2])
        dataX.append(xset)
    return np.array(dataX), np.array(dataY)


look_back = 15
x_train1, y_train1 = create_dataset(dataset1, look_back)
x_train2, y_train2 = create_dataset(dataset2, look_back)
x_train3, y_train3 = create_dataset(dataset3, look_back)
x_validate, y_validate = create_dataset(dataset4, look_back)
x_test, y_test = create_dataset(dataset5, look_back)


# 入力データは3列
n_in = 3
# 出力データは予測値一つ
n_out = 1

# LSTMで使用する形に整形
x_train1 = np.reshape(x_train1, (x_train1.shape[0], x_train1.shape[1], x_train1.shape[2]))
y_train1 = np.array(y_train1).reshape(len(y_train1), n_out)

x_train2 = np.reshape(x_train2, (x_train2.shape[0], x_train2.shape[1], x_train2.shape[2]))
y_train2 = np.array(y_train2).reshape(len(y_train2), n_out)

x_train3 = np.reshape(x_train3, (x_train3.shape[0], x_train3.shape[1], x_train3.shape[2]))
y_train3 = np.array(y_train3).reshape(len(y_train3), n_out)

x_validate = np.reshape(x_validate, (x_validate.shape[0], x_validate.shape[1], x_validate.shape[2]))
y_validate = np.array(y_validate).reshape(len(y_validate), n_out)

x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], x_test.shape[2]))
y_test = np.array(y_test).reshape(len(y_test), n_out)


# 隠れ層
n_hidden = 100
length_of_sequence = 15
in_out_neurons = 1
epoch = 100


# モデルの設定
model = Sequential()
model.add(
  LSTM(
    n_hidden,
    input_shape=(x_test.shape[1], look_back),
    return_sequences=False
  )
)
model.add(Dense(in_out_neurons))
model.add(Activation("linear"))
optimizer = Adam(lr=0.001)
model.compile(loss="mean_squared_error", optimizer=optimizer)


# 学習
early_stopping = EarlyStopping(monitor='val_loss', mode='auto', patience=10)
history = model.fit(
  x_train1,
  y_train1,
  batch_size=32,
  epochs=epoch,
  validation_data=(x_validate, y_validate)
)

history = model.fit(
  x_train2,
  y_train2,
  batch_size=32,
  epochs=epoch,
  validation_data=(x_validate, y_validate)
)

history = model.fit(
  x_train3,
  y_train3,
  batch_size=32,
  epochs=epoch,
  validation_data=(x_validate, y_validate)
)


# 予測
test_predict = model.predict(x_test)
print(model.evaluate(x_test, y_test))
pad_col = np.zeros(dataset1.shape[1]-1)


def pad_array(val):
    return np.array([np.insert(pad_col, 0, x) for x in val])


test_predict = scaler.inverse_transform(pad_array(test_predict))
y_test = scaler.inverse_transform(pad_array(y_test))

plt.figure()
plt.plot(
  range(length_of_sequence, len(test_predict) + length_of_sequence),
  test_predict[:, 0], color="r", label="predict_data"
  )
plt.plot(range(0, len(y_test)), y_test[:, 0], color="b", label="row_data")
plt.legend()
plt.show()
