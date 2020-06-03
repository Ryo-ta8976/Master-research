from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# CSVファイルの読み込み
df = pd.read_csv('../data_2014-2017.csv')
print(df.isnull().sum())

# 欠損値の穴埋め
df = df.fillna(method='ffill')
print(df.isnull().sum())

df = df["snow"]
print(df)

# データの生成
data = []
target = []

# 過去遡る日数
max_len = 10
# 将来予測する日数
future = 1
# 入力データは一列
n_in = 1
# 出力データは予測値一つ
n_out = 1

# LSTMでのデータ構造に変更
for i in range(len(df) - max_len):
    data.append(df[i:i + max_len])
    target.append(df[i + max_len])

# LSTMで使用する形に整形
data = np.array(data).reshape(len(data), max_len, n_in)
target = np.array(target).reshape(len(target), n_out)

# データの分割
x_train, x_test = train_test_split(data, test_size=0.2, shuffle=False)
y_train, y_test = train_test_split(target, test_size=0.2, shuffle=False)

# 隠れ層
n_hidden = 10
length_of_sequence = 10
in_out_neurons = 1

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
early_stopping = EarlyStopping(monitor='val_loss', mode='auto', patience=20)
history = model.fit(
  x_train,
  y_train,
  batch_size=32,
  epochs=100,
  validation_data=(x_test, y_test)
)

# 予測
test_predict = model.predict(x_test)
plt.figure()
plt.plot(
  range(length_of_sequence, len(test_predict) + length_of_sequence),
  test_predict, color="r", label="predict_data"
  )
plt.plot(range(0, len(y_test)), y_test, color="b", label="row_data")
plt.legend()
plt.show()
