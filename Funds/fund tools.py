import numpy as np
import pandas as pd
import akshare as ak

def get_fund_categories(open_fund=False):

    fund_em_fund_name_df = ak.fund_em_fund_name()

    if open_fund:
        fund_em_open_fund_daily_df = ak.fund_em_open_fund_daily()
        df = pd.merge(fund_em_open_fund_daily_df, fund_em_fund_name_df, on='基金代码')

        fund_categories = np.unique(df['基金类型'].values)
    else:
        fund_categories = np.unique(fund_em_fund_name_df['基金类型'].values)

    return fund_categories


def get_category_all_funds(category):

    df = ak.fund_em_fund_name()
    df = df[df['基金类型'] == category]

    fund_code = df['基金代码'].values

    return df, fund_code


def get_fund_net_worth(fund_code, start_date, end_date, fund_category):

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')

    if fund_category == 'open':
        df = ak.fund_em_open_fund_info(fund=fund_code)
    elif fund_category == 'money':
        df = ak.fund_em_money_fund_info(fund=fund_code)
        df['净值日期'] = pd.to_datetime(df['净值日期'], format='%Y/%m/%d')
    elif fund_category == 'financial':
        df = ak.fund_em_financial_fund_info(fund=fund_code)
        df['净值日期'] = pd.to_datetime(df['净值日期'], format='%Y/%m/%d')
    elif fund_category == 'etf':
        df = ak.fund_em_etf_fund_info(fund=fund_code)
        df['净值日期'] = pd.to_datetime(df['净值日期'], format='%Y/%m/%d')

    mask = (df['净值日期'] >= start_date) & (df['净值日期'] <= end_date)
    df = df.loc[mask].reset_index().drop('index', axis=1)

    return df

def get_fund_cumulative_return(fund_code, start_date, end_date):

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')

    df = ak.fund_em_open_fund_info(fund=fund_code, indicator="累计收益率走势")
    mask = (df['净值日期'] > start_date) & (df['净值日期'] <= end_date)
    df = df.loc[mask].reset_index().drop('index', axis=1)

    return df




