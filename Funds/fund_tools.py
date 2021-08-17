import numpy as np
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc("font",family='PingFang HK')


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


def sw_industry_return_plot(start_date, end_date, year_start_date='2021-01-01'):

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')
    year_start_date = pd.to_datetime(year_start_date, format='%Y/%m/%d')

    industry_name = ak.sw_index_spot()['指数名称'].values
    industry_code = ak.sw_index_spot()['指数代码'].values

    industry_return_df = pd.DataFrame()
    industry_yearly_return = []
    industry_weekly_return = []

    for i in range(len(industry_code)):
        df1 = ak.sw_index_daily(industry_code[i], start_date, end_date)
        temp_df1 = df1.set_index('index_code').iloc[:, 3:].astype(float)['close']
        industry_return = (temp_df1[0] - temp_df1[-1])/temp_df1[-1]
        industry_weekly_return.append(industry_return)

        df2 = ak.sw_index_daily(industry_code[i], year_start_date, end_date)
        temp_df2 = df2.set_index('index_code').iloc[:, 3:].astype(float)['close']
        industry_return = (temp_df2[0] - temp_df2[-1])/temp_df2[-1]
        industry_yearly_return.append(industry_return)

    industry_return_df['Industry'] = industry_name
    industry_return_df['WeeklyReturn'] = industry_weekly_return
    industry_return_df['YearlyReturn'] = industry_yearly_return
    industry_return_df.index = industry_code

    fig = plt.figure(figsize=(15,10))

    plt.subplot(1,2,1)
    industry_return_df.sort_values('WeeklyReturn', ascending=True, inplace=True)
    plt.barh(industry_return_df.Industry, industry_return_df.WeeklyReturn)
    for i in range(len(industry_return_df.WeeklyReturn)):
        value_label = str(industry_return_df.WeeklyReturn[i]*100)[:5] + '%'
        plt.annotate(value_label, xy=(industry_return_df.WeeklyReturn[i],
                                      industry_return_df.Industry[i]), ha='center', va='center', size=15, color='r')
    plt.title(r'本周收益率')
    plt.yticks(industry_return_df.Industry, fontproperties = 'PingFang HK',fontsize = 15);

    plt.subplot(1,2,2)
    industry_return_df.sort_values('YearlyReturn', ascending=True, inplace=True)
    plt.barh(industry_return_df.Industry, industry_return_df.YearlyReturn)
    for i in range(len(industry_return_df.WeeklyReturn)):
        value_label = str(industry_return_df.YearlyReturn[i]*100)[:5] + '%'
        plt.annotate(value_label, xy=(industry_return_df.YearlyReturn[i],
                                      industry_return_df.Industry[i]), ha='center', va='center', size=15, color='r')
    plt.title(r'今年以来收益率')
    plt.yticks(industry_return_df.Industry, fontproperties = 'PingFang HK',fontsize = 15);

    return industry_return_df



