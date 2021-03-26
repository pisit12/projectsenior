
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from fbprophet import Prophet
import statsmodels.api as sm # Time series analysis
import datetime

from sklearn.metrics import r2_score

pd.plotting.register_matplotlib_converters()
mpl.rcParams['figure.figsize'] = (20, 10)
sns.set()
df = pd.read_csv('.seniorProject/weather/weather_forecast.csv',
                           parse_dates=True,usecols=['date_time','temp_avg','name'])

df.head()

train_df = df.reset_index()
train_df = train_df.rename(columns={"date_time": "ds", "TAVG": "y"})

model = Prophet()
model.fit(train_df)


test_df = df.rename(columns={"date_time": "ds", "TAVG": "y"})
test_pred = model.predict(test_df)

model_score = r2_score(test_df["y"], test_pred["yhat"])
print(model_score)


future_df = model.make_future_dataframe(periods=1) # +1 year of data!
prediction = model.predict(future_df)
model.plot_components(prediction)

ax6 = prediction.plot(x="ds", y="yhat")
ax6.set_xlim(pd.Timestamp("2020-01-01"), pd.Timestamp("2021-03-31"))
ax6.set_xlabel("Date (YYYY-MM)")
ax6.set_ylabel("Temperature (C)")
ax6.set_title("Temperature Predictions for 2020-2021")















#
# def vis(df):
#     ax = df.plot()
#     ax.set_xlim(pd.Timestamp("2021-03-01"), pd.Timestamp("2021-03-31"))
#     ax.set_title("2021 KATL Average Air Temperature")
#     ax.set_xlabel("Date (YYYY-MM)")
#     ax.set_ylabel("Average Temperature (C)")
# vis(df)
#
# def show_seasonal_decompose(df):
#     decomp = sm.tsa.seasonal_decompose(df, model="additive", freq=365)
#     decomp.plot()
# show_seasonal_decompose(df)
#
# def plot_yearly_avg(df):
#     df_cpy = df.copy()
#     df_cpy = df.sort_index()
#
#     g = df_cpy.groupby(df.index.year)["temp_avg"].mean()
#     g = g.drop(g.tail(1).index) # We only keep data up to 2019 since 2020 data is imcomplete
#
#     ax = g.plot()
#     ax.set_title("Yearly Average Air Temperature at KATL")
#     ax.set_xlabel("Year")
#     ax.set_ylabel("Temperature (C)")
# plot_yearly_avg(df)
#
#
# def print_stats(df):
#     df_cpy = df.copy()
#     X = df_cpy.values
#     split = len(X) // 2
#     X1, X2 = X[0: split], X[split:]
#     mean1, mean2 = X1.mean(), X2.mean()
#     var1, var2 = X1.var(), X2.var()
#     print("Mean: X1 = {}, X2 = {}".format(mean1, mean2))
#     print("Variance: X1 = {}, X2 = {}".format(var1, var2))
#
# print_stats(df)
#
# def plot_dist(df):
#     ax = df.hist()
#     ax[0][0].set_title("Average Air Temperature Distribution at KATL")
#     ax[0][0].set_xlabel("Count")
#     ax[0][0].set_ylabel("Temperature (C)")
#
# plot_dist(df)
#
#
# def print_adfuller(df):
#     df_cpy = df.copy()
#     print("Dickey-Fuller Test")
#     results = sm.tsa.stattools.adfuller(df_cpy["temp_avg"])
#     print("df (test Statistic) = {}".format(results[0]))
#     print("pvalue = {}".format(results[1]))
#     print("lags = {}".format(results[2]))
#     print("nobs = {}".format(results[3]))
#
#     for key, value in results[4].items():
#         print("{} = {}".format(key, value))
#
# print_adfuller(df)
#
# def print_kpss(df):
#     df_cpy = df.copy()
#     print("KPSS Test")
#     results = sm.tsa.stattools.kpss(df_cpy["temp_avg"], regression="c", lags="auto")
#     print("df (test Statistic) = {}".format(results[0]))
#     print("pvalue = {}".format(results[1]))
#     print("lags = {}".format(results[2]))
#
#     for key, value in results[3].items():
#         print("{} = {}".format(key, value))
# print_kpss(df)



# pd.plotting.register_matplotlib_converters()
#         plt.rcParams['figure.figsize'] = (20, 10)
#         # plt.style.use('ggplot')
#         sns.set()
#         df = pd.read_csv('./weather/weather_forecast.csv',
#                            parse_dates=True,usecols=['date_time','temp_avg','name'])
#         train_df = df.reset_index()
#         train_df = train_df.rename(columns={"date_time": "ds", "temp_avg": "y"})
#         model = Prophet(
#                 weekly_seasonality = True,
#                 daily_seasonality = True,
#                 )
#         model.fit(train_df)
#         test_df = train_df.rename(columns={"date_time": "ds", "temp_avg": "y"})
#         test_pred = model.predict(test_df)
#
#         model_score = r2_score(train_df["y"], test_pred["yhat"])
#         print(model_score)
#         test_df = model.make_future_dataframe(periods=1)
#         test_df['cap'] = 50
#         # future.tail(5)
#         fcst = model.predict(test_df)
#         print(fcst)