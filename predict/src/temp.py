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
df1 = pd.read_csv('../split_data_2014_2015.csv')
df2 = pd.read_csv('../split_data_2015_2016.csv')
df3 = pd.read_csv('../split_data_2016_2017.csv')
df4 = pd.read_csv('../split_data_2017_2018.csv')
df5 = pd.read_csv('../split_data_2018_2019.csv')


# 欠損値の穴埋め
df1 = df1.fillna(method='ffill')
df2 = df2.fillna(method='ffill')
df3 = df3.fillna(method='ffill')
df4 = df4.fillna(method='ffill')
df5 = df5.fillna(method='ffill')


df1 = df1["積雪量"]
df2 = df2["積雪量"]
df3 = df3["積雪量"]
df4 = df4["積雪量"]
df5 = df5["積雪量"]

# データの標準化
scaler = MinMaxScaler()
df1 = np.array(scaler.fit_transform(np.array(df1).reshape(-1, 1))).reshape(1, -1)
df1 = np.array(scaler.fit_transform(np.array(df2).reshape(-1, 1))).reshape(1, -1)
df3 = np.array(scaler.fit_transform(np.array(df3).reshape(-1, 1))).reshape(1, -1)
df4 = np.array(scaler.fit_transform(np.array(df4).reshape(-1, 1))).reshape(1, -1)
df5 = np.array(scaler.fit_transform(np.array(df5).reshape(-1, 1))).reshape(1, -1)

# データの生成
data1 = []
target1 = []
data2 = []
target2 = []
data3 = []
target3 = []
data4 = []
target4 = []
data5 = []
target5 = []

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

for i in range(len(df4) - max_len):
    data4.append(df4[i:i + max_len])
    target4.append(df4[i + max_len])

for i in range(len(df5) - max_len):
    data5.append(df5[i:i + max_len])
    target5.append(df5[i + max_len])

# LSTMで使用する形に整形
data1 = np.array(data1).reshape(len(data1), max_len, n_in)
target1 = np.array(target1).reshape(len(target1), n_out)

data2 = np.array(data2).reshape(len(data2), max_len, n_in)
target2 = np.array(target2).reshape(len(target2), n_out)

data3 = np.array(data3).reshape(len(data3), max_len, n_in)
target3 = np.array(target3).reshape(len(target3), n_out)

data4 = np.array(data4).reshape(len(data4), max_len, n_in)
target4 = np.array(target4).reshape(len(target4), n_out)

data5 = np.array(data5).reshape(len(data5), max_len, n_in)
target5 = np.array(target5).reshape(len(target5), n_out)

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
  validation_data=(data4, target4)
)

history = model.fit(
  data2,
  target2,
  batch_size=32,
  epochs=epoch,
  validation_data=(data4, target4)
)

history = model.fit(
  data3,
  target3,
  batch_size=32,
  epochs=epoch,
  validation_data=(data4, target4)
)

# 予測
test_predict = model.predict(data5)
print(model.evaluate(data5, target5))
plt.figure()
plt.plot(
  range(length_of_sequence, len(test_predict) + length_of_sequence),
  test_predict, color="r", label="predict_data"
  )
plt.plot(range(0, len(target5)), target5, color="b", label="row_data")
plt.legend()
plt.show()
