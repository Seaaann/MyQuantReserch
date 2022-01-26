import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak
from datetime import date, timedelta
import seaborn as sns
import statsmodels.api as sm

from fund_tools import *
from AIP import *

matplotlib.rc("font", family="PingFang HK")

# make a plot with fund net worth and base


def fund_vs_benchmark(fund, benchmark_list, start_date, end_date, PLOT=True):

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    stock_zh_index_spot_df = ak.stock_zh_index_spot()[['代码', '名称']]

    fund_value = get_fund_net_worth(fund,
                                    start_date=start_date,
                                    end_date=end_date,
                                    fund_category='open').set_index('净值日期')
    benchmark_df = pd.DataFrame()
    index_list = []
    for benchmark in benchmark_list:

        benchmark_index = ak.stock_zh_index_daily(symbol=benchmark)[[
            'date', 'close'
        ]]
        benchmark_index = benchmark_index.loc[
            (benchmark_index['date'] >= start_date)
            & (benchmark_index['date'] <= end_date)]
        benchmark_index[benchmark] = benchmark_index['close'].values[0]
        benchmark_index[
            benchmark] = benchmark_index['close'] / benchmark_index[benchmark]
        benchmark_index = benchmark_index.set_index('date')
        benchmark_df = pd.concat([benchmark_df, benchmark_index], axis=1)

        index_list.append(stock_zh_index_spot_df[stock_zh_index_spot_df['代码']
                                                 == benchmark]['名称'].values[0])
    fund_value = fund_value.join(benchmark_df[benchmark_list])

    fund_value['基准指数'] = 0.05 * fund_value[
        benchmark_list[0]] + 0.95 * fund_value[benchmark_list[1]]
    index_list.append('基准指数')
    benchmark_list.append('基准指数')

    if PLOT:
        fig = plt.figure(figsize=(12, 8))

        for i in range(len(index_list)):
            plt.plot(fund_value[benchmark_list[i]], label=index_list[i])
        plt.plot(fund_value['单位净值'], label='基金净值')
        plt.legend()
        plt.title('基金累计收益率与基准指数收益对比')

    return fund_value


def Fund_Perform_Attribution(df):

    result = {}
    X = df.iloc[:, 2:]
    X = sm.add_constant(X)
    y = df['ret']

    model_fit = sm.OLS(y, X).fit()

    print(model_fit.summary())


def transto_monthlyreturn(df):

    return_bar_df = pd.DataFrame()
    return_list = []
    df['year'] = pd.DatetimeIndex(df['净值日期']).year
    df['month'] = pd.DatetimeIndex(df['净值日期']).month
    year_list = df['year'].unique()

    for year in year_list:
        month_list = df[df['year'] == year]['month'].unique()
        for month in month_list:
            sub_df = df[(df['year'] == year) & (df['month'] == month)]
            timestamp = pd.to_datetime(str(year) + '-' + str(month))
            return_list.append(
                (sub_df['单位净值'].values[-1] / sub_df['单位净值'].values[0] - 1) *
                100)
            return_bar_df[timestamp] = 0

    return_bar_df = return_bar_df.T
    return_bar_df['ret'] = return_list
    return return_bar_df


def transto_monthlyindex(df):

    index_bar_df = pd.DataFrame()
    index_list = []
    df['year'] = pd.DatetimeIndex(df['净值日期']).year
    df['month'] = pd.DatetimeIndex(df['净值日期']).month
    year_list = df['year'].unique()

    for year in year_list:
        month_list = df[df['year'] == year]['month'].unique()
        for month in month_list:
            sub_df = df[(df['year'] == year) & (df['month'] == month)]
            timestamp = pd.to_datetime(str(year) + '-' + str(month))
            index_list.append((sub_df['单位净值'].values[-1]))
            index_bar_df[timestamp] = 0

    index_bar_df = index_bar_df.T
    index_bar_df['Value'] = index_list
    return index_bar_df