import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak
import datetime
from datetime import date, timedelta
import seaborn as sns
import time
import random
import itertools

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
