import numpy as np
import pandas as pd
import akshare as ak

def get_fund_categories():

    fund_em_fund_name_df = ak.fund_em_fund_name()
    fund_categories = np.unique(fund_em_fund_name_df['基金类型'].values)

    return fund_categories


def get_category_all_funds(category):

    df = ak.fund_em_fund_name()
    df = df[df['基金类型'] == category]

    fund_code = df['基金代码'].values

    return df, fund_code


def get_fund_net_worth(fund_code, start_date, end_date):

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')

    df = ak.fund_em_open_fund_info(fund=fund_code)
    mask = (df['净值日期'] > start_date) & (df['净值日期'] <= end_date)
    df = df.loc[mask].reset_index().drop('index', axis=1)

    return df

