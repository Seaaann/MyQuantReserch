from heapq import merge
import numpy as np
import pandas as pd
import math

from fund_tools import get_risk_free_rate


def return_metrics(df, risk_free=False):

    abs_return = (df['单位净值'].values[-1] -
                  df['单位净值'].values[0]) / df['单位净值'].values[0]
    annual_return = (1 + abs_return)**(252 / len(df)) - 1

    return abs_return, annual_return


def max_drawdown(df):

    roll_max = df['单位净值'].rolling(len(df), 1).max()
    daliy_drawdown = df['单位净值'] / roll_max - 1.0
    max_daily_drawdown = daliy_drawdown.rolling(len(df), 1).min()

    return max_daily_drawdown.values[-1]


def risk_metrics(df):

    annual_volatility = df['日增长率'].std() * (252**0.5)

    max_daily_drawdown = max_drawdown(df)

    return annual_volatility, max_daily_drawdown


def sharpe(df):

    risk_free = get_risk_free_rate(df['净值日期'].values[0], df['净值日期'].values[-1])
    df = df.set_index('净值日期')
    risk_free = risk_free.set_index('日期')
    merged_df = df.join(risk_free)
    merged_df['中国国债收益率10年'] = merged_df['中国国债收益率10年'] / 100

    annual_sharpe = (
        (merged_df['日增长率'].mean() - merged_df['中国国债收益率10年'].mean()) /
        merged_df['日增长率'].std()) * (len(df)**0.5)

    return annual_sharpe


def calmar(df):

    calmar_ratio = return_metrics(df)[1] / max_drawdown(df)

    return calmar_ratio


def win_rate(df):

    df['win'] = True
    for i in range(len(df) - 1):
        if df['单位净值'][i + 1] / df['单位净值'][i] < 1.0:
            df['win'][i + 1] = False

    win_rate = len(df[df['win'] == True]) / len(df)
    return win_rate