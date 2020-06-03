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
df1 = pd.read_csv('../data_2014-2017.csv')
df2 = pd.read_csv('../data_2017-2018.csv')
df3 = pd.read_csv('../data_2018-2019.csv')


# 欠損値の穴埋め
df1 = df1.fillna(method='ffill')
df2 = df2.fillna(method='ffill')
df3 = df3.fillna(method='ffill')


df1 = df1["snow"]
df2 = df2["snow"]
df3 = df3["snow"]


# データの生成
data1 = []
target1 = []
data2 = []
target2 = []
data3 = []
target3 = []


# 過去遡る日数
max_len = 15
# 将来予測する日数
future = 1
# 入力データは一列
n_in = 1
# 出力データは予測値一つ
n_out = 1

# LSTMでのデータ構造に変更
for i in range(len(df1) - max_len):
    data1.append(df1[i:i + max_len])
    target1.append(df1[i + max_len])

for i in range(len(df2) - max_len):
    data2.append(df2[i:i + max_len])
    target2.append(df2[i + max_len])

for i in range(len(df3) - max_len):
    data3.append(df3[i:i + max_len])
    target3.append(df3[i + max_len])


# LSTMで使用する形に整形
data1 = np.array(data1).reshape(len(data1), max_len, n_in)
target1 = np.array(target1).reshape(len(target1), n_out)

data2 = np.array(data2).reshape(len(data2), max_len, n_in)
target2 = np.array(target2).reshape(len(target2), n_out)

data3 = np.array(data3).reshape(len(data3), max_len, n_in)
target3 = np.array(target3).reshape(len(target3), n_out)


# 隠れ層
n_hidden = 150
length_of_sequence = 15
in_out_neurons = 1
epoch = 100

# モデルの設定
model = Sequential()
model.add(
  LSTM(
    n_hidden,
    batch_input_shape=(None, length_of_sequence, in_out_neurons),
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
  data1,
  target1,
  batch_size=32,
  epochs=epoch,
  validation_data=(data2, target2)
)


# 予測
test_predict = model.predict(data3)
print(model.evaluate(data3, target3))
plt.figure()
plt.plot(
  range(length_of_sequence, len(test_predict) + length_of_sequence),
  test_predict, color="r", label="predict_data"
  )
plt.plot(range(0, len(target3)), target3, color="b", label="row_data")
plt.legend()
plt.show()
