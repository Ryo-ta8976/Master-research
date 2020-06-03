import numpy as np
import matplotlib.pyplot as plt
# グラフを横長にする
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import statsmodels.api as sm


# CSVファイルの読み込み
df = pd.read_csv('../sample.csv')
df.snow = df.snow.astype('float64')
df.date = pd.to_datetime(df.date)
df = df.set_index('date')
print(df.head())

# plt.figure()
# plt.plot(data.snow)
# plt.legend()
# plt.show()

#  自己相関のグラフ
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df.snow, lags=75, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df.snow, lags=75, ax=ax2)


# plt.plot(data.snow)
plt.show()
