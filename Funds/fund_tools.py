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
    """

    :param fund_code: string, input a fund code
    :param start_date: string, input a date format 'yyyy-mm-dd'
    :param end_date: string, input a date format 'yyyy-mm-dd'
    :param fund_category: string, input either ['open', 'money', 'financial', 'etf']
    :return: dataframe, sliced dataframe between start_date and end_date
    """

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

def get_open_fund_rank(category, rank, order_by, ascending=False):

    """
    :param category: string, input ['股票型','混合型',"指数型",'QDII','LOF','FOF' ]
    :param rank: int, return how many rows of the dataframe
    :param order_by: string, input ['近1周', '近1月', '近3月',
       '近6月', '近1年', '近2年', '近3年']
    :param ascending: bool, default False
    :return: dataframe, with specific sorted dataframe
    """

    if category == '股票型':
        df = ak.fund_em_open_fund_rank(symbol="股票型")
    elif category == '混合型':
        df = ak.fund_em_open_fund_rank(symbol="混合型")
    elif category == '债券型':
        df = ak.fund_em_open_fund_rank(symbol="债券型")
    elif category == "指数型":
        df = ak.fund_em_open_fund_rank(symbol="指数型")
    elif category == 'QDII':
        df = ak.fund_em_open_fund_rank(symbol="QDII")
    elif category == 'LOF':
        df = ak.fund_em_open_fund_rank(symbol="LOF")
    elif category == 'FOF':
        df = ak.fund_em_open_fund_rank(symbol="FOF")

    df = df.sort_values(by=[order_by], ascending=ascending)

    return df.head(rank)

def get_etf_rank(rank, order_by, ascending=False):

    """
    :param rank: int, return how many rows of the dataframe
    :param order_by: string, input ['近1周', '近1月', '近3月', '近6月',
       '近1年', '近2年', '近3年', '今年来', '成立来']
    :param ascending: bool, default False
    :return: dataframe, with specific sorted dataframe
    """

    df = ak.fund_em_exchange_rank()

    df = df.sort_values(by=[order_by], ascending=ascending)

    return df.head(rank)


def get_money_fund_rank(rank, order_by, ascending=False):

    """
    :param rank: int, return how many rows of the dataframe
    :param order_by: string, input ['万份收益', '年化收益率7日', '年化收益率14日', '年化收益率28日',
       '近1月', '近3月', '近6月', '近1年', '近2年', '近3年', '近5年', '今年来', '成立来']
    :param ascending: bool, default False
    :return: dataframe, with specific sorted dataframe
    """

    df = ak.fund_em_money_rank()

    df = df.sort_values(by=[order_by], ascending=ascending)

    return df.head(rank)


def get_fund_cumulative_return(fund_code, start_date, end_date):

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')

    df = ak.fund_em_open_fund_info(fund=fund_code, indicator="累计收益率走势")
    mask = (df['净值日期'] > start_date) & (df['净值日期'] <= end_date)
    df = df.loc[mask].reset_index().drop('index', axis=1)

    return df




