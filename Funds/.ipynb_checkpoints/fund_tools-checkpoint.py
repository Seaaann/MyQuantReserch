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
    :param category: string, input ['股票型','混合型',"指数型",'QDII','LOF','FOF']
    :param rank: int, return how many rows of the dataframe
    :param order_by: string, input ['近1周', '近1月', '近3月',
       '近6月', '近1年', '近2年', '近3年']
    :param ascending: bool, default False
    :return: dataframe, with specific sorted dataframe
    """

    if category == '股票型':
        df = ak.fund_em_open_fund_rank(symbol="股票型").sort_values(by=[order_by], ascending=ascending)
    elif category == '混合型':
        df = ak.fund_em_open_fund_rank(symbol="混合型").sort_values(by=[order_by], ascending=ascending)
    elif category == '债券型':
        df = ak.fund_em_open_fund_rank(symbol="债券型").sort_values(by=[order_by], ascending=ascending)
    elif category == "指数型":
        df = ak.fund_em_open_fund_rank(symbol="指数型").sort_values(by=[order_by], ascending=ascending)
    elif category == 'QDII':
        df = ak.fund_em_open_fund_rank(symbol="QDII").sort_values(by=[order_by], ascending=ascending)
    elif category == 'LOF':
        df = ak.fund_em_open_fund_rank(symbol="LOF").sort_values(by=[order_by], ascending=ascending)
    elif category == 'FOF':
        df = ak.fund_em_open_fund_rank(symbol="FOF").sort_values(by=[order_by], ascending=ascending)

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

    df = ak.fund_em_money_rank().sort_values(by=[order_by], ascending=ascending)
    return df.head(rank)


def get_fund_cumulative_return(fund_code, start_date, end_date):

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')

    df = ak.fund_em_open_fund_info(fund=fund_code, indicator="累计收益率走势")
    mask = (df['净值日期'] > start_date) & (df['净值日期'] <= end_date)
    df = df.loc[mask].reset_index().drop('index', axis=1)

    return df


def sw_industry_return_plot(start_date, end_date, year_start_date='2021-01-01', save_pic=True):

    """
    :param start_date: string, start date of the week
    :param end_date: string, end date of the week
    :param year_start_date: string, start date of the year
    :param save_pic: bool, save picture or not
    :return: dataframe
    """

    startDate = pd.to_datetime(start_date, format='%Y/%m/%d')
    endDate = pd.to_datetime(end_date, format='%Y/%m/%d')
    year_start_date = pd.to_datetime(year_start_date, format='%Y/%m/%d')

    industry_name = ak.sw_index_spot()['指数名称'].values
    industry_code = ak.sw_index_spot()['指数代码'].values

    industry_return_df = pd.DataFrame()
    industry_yearly_return = []
    industry_weekly_return = []

    for i in range(len(industry_code)):
        df1 = ak.sw_index_daily(industry_code[i], startDate, endDate)
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

    matplotlib.rc("font",family='PingFang HK')


    fig = plt.figure(figsize=(15,10))

    plt.subplot(1,2,1)
    industry_return_df.sort_values('WeeklyReturn', ascending=True, inplace=True)
    plt.barh(industry_return_df.Industry, industry_return_df.WeeklyReturn)
    for i in range(len(industry_return_df.WeeklyReturn)):
        value_label = str(industry_return_df.WeeklyReturn[i]*100)[:5] + '%'
        plt.annotate(value_label, xy=(industry_return_df.WeeklyReturn[i],
                                      industry_return_df.Industry[i]), ha='center', va='center', size=15, color='r')
    plt.title(r'本周收益率' + str(start_date) + '~' + str(end_date))
    plt.yticks(industry_return_df.Industry, fontproperties = 'PingFang HK',fontsize = 15);

    plt.subplot(1,2,2)
    industry_return_df.sort_values('YearlyReturn', ascending=True, inplace=True)
    plt.barh(industry_return_df.Industry, industry_return_df.YearlyReturn)
    for i in range(len(industry_return_df.WeeklyReturn)):
        value_label = str(industry_return_df.YearlyReturn[i]*100)[:5] + '%'
        plt.annotate(value_label, xy=(industry_return_df.YearlyReturn[i],
                                      industry_return_df.Industry[i]), ha='center', va='center', size=15, color='r')
    plt.title(r'今年以来收益率'+ str((year_start_date.year)))
    plt.yticks(industry_return_df.Industry, fontproperties = 'PingFang HK',fontsize = 15);

    if save_pic:
        plt.savefig('申万行业收益率.png', dpi=500)

    return industry_return_df


def get_index_price(code, start_date, end_date, year_start_date='2021-01-01'):

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')
    year_start_date = pd.to_datetime(year_start_date, format='%Y/%m/%d')

    df = ak.stock_zh_index_daily(symbol=code).reset_index()
    df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')
    df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None))
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    df = df.loc[mask].set_index('date')

    return df

def get_index_code_and_name():

    name_code_dict = ak.stock_zh_index_spot().set_index('名称')['代码'].to_dict()

    return name_code_dict


def main_index_plot(code_list, start_date, end_date, year_start_date='2021-01-01', save_pic=True):

    index_df = pd.DataFrame()
    for code in code_list:
        closePrice = get_index_price(code, start_date, end_date)['close']
        index_df[code] = closePrice

    fig,ax = plt.subplots(figsize=(12,8))

    ax.plot(df.index, df.sh000001, label='上证指数')
    ax.plot(df.index, df.sz399006, label='创业板指')

    ax.set_ylabel('上证&创业扳指', size=15)

    ax.legend()

    ax.set_xlabel("year",fontsize=14)

    ax2=ax.twinx()
    ax2.plot(df.index, df.sh000300, 'g-', label='沪深300')
    ax2.set_ylabel('沪深300', size=15)
    ax2.legend(loc=2)

    if save_pic:
        plt.savefig('主要指数走势.png', dpi=500)

    return index_df


def current_open_fund_mergered():
    
    fund_em_open_fund_daily_df = ak.fund_em_open_fund_daily()
    fund_em_fund_name_df = ak.fund_em_fund_name()
    
    df = pd.merge(fund_em_open_fund_daily_df, fund_em_fund_name_df, on='基金代码')
    column_list = [0,1,2,3,4,5,6,7,8,9,10,13]    
    
    df = df.iloc[:, column_list]
    
    df['基金大类'] = np.nan
    l = ['债券型-中短债', '债券型-可转债', '债券型-混合债', '债券型-长债', '指数型-股票', 
     '混合型-偏债', '混合型-偏股', '混合型-平衡', '混合型-灵活', '股票型' ]
    
    for i in range(len(df)):
        if df['基金类型'].values[i] in l:
            df['基金大类'][i] = df['基金类型'].values[i][0:3]
        else:
            df['基金大类'][i] = df['基金类型'].values[i]

    
    return df



def AIP_Weekly(code, start_date, end_date, fund_category, fixed_investment, freq='Monday', df=False, AIP=True, Total_investment=100000):
    
    
    fund_net_value = get_fund_net_worth(code, start_date=start_date, end_date=end_date, fund_category=fund_category)
    
    fund_net_value['WeekDay'] = pd.to_datetime(fund_net_value['净值日期']).dt.day_name()
    
    
    if AIP:
        fund_net_value['定投金额(本金)'] = 0
            
        for i in range(len(fund_net_value['WeekDay'])):
             if fund_net_value['WeekDay'].values[i] == freq:
                    fund_net_value['定投金额(本金)'][i] = fixed_investment
                
        fund_net_value['累计定投金额(本金)'] = fund_net_value['定投金额(本金)'].cumsum()
        fund_net_value['购买份额'] = fund_net_value['定投金额(本金)']/fund_net_value['单位净值']
        fund_net_value['累计份额'] = fund_net_value['购买份额'].cumsum()
        fund_net_value['平均成本'] = fund_net_value['累计定投金额(本金)']/fund_net_value['累计份额']
    
        fund_net_value['累计收益'] = (fund_net_value['单位净值'] - fund_net_value['平均成本']) * fund_net_value['累计份额']
        
        start_invest = fund_net_value['定投金额(本金)'].values.nonzero()[0][0]
        fund_net_value['持有天数(定投)'] = (fund_net_value['净值日期'] - fund_net_value['净值日期'][start_invest]).dt.days+1
        for i in range(len(fund_net_value['持有天数(定投)'])):
            if fund_net_value['持有天数(定投)'][i] < 0:
                fund_net_value['持有天数(定投)'][i] = 0
        fund_net_value['年化收益率'] = ((fund_net_value['累计收益'] + fund_net_value['累计定投金额(本金)'])/fund_net_value['累计定投金额(本金)'])**(365/fund_net_value['持有天数(定投)'])-1
        fund_net_value['累计收益率'] = fund_net_value['累计收益']/fund_net_value['累计定投金额(本金)']
        
        Stat_df = pd.DataFrame({
                '基金代码': code,
                '持有天数': fund_net_value['持有天数(定投)'].values[-1],
                '定投时间': freq,
                '定投金额': fixed_investment,
                '分投期数': fund_net_value['累计定投金额(本金)'].values[-1]/fixed_investment,
                '总购买份额' : '%.3f' % fund_net_value['累计份额'].values[-1],
                '平均成本' : '%.3f' % fund_net_value['平均成本'].values[-1],
                '累计收益' : '%.3f' % fund_net_value['累计收益'].values[-1],
                '累计收益率' : '%.3f' % fund_net_value['累计收益率'].values[-1],
                '年化收益率' : '%.3f' % fund_net_value['年化收益率'].values[-1]
            }, index=['AIP'])
    
    else:
        fund_net_value['直投金额(本金)'] = 0
        fund_net_value['直投金额(本金)'][0] = Total_investment
        fund_net_value['直投累计购买份额(不变)'] = fund_net_value['直投金额(本金)'][0]/ fund_net_value['单位净值'][0]
        fund_net_value['直投累计收益'] = (fund_net_value['单位净值'] - fund_net_value['单位净值'][0]) * fund_net_value['直投金额(本金)'][0]
        fund_net_value['直投累计收益率'] = fund_net_value['直投累计收益']/fund_net_value['直投累计购买份额(不变)']
        fund_net_value['持有天数(直投)'] = (fund_net_value['净值日期'] - fund_net_value['净值日期'][0]).dt.days+1
        fund_net_value['直投累计年化收益率'] = ((fund_net_value['直投金额(本金)'][0] + fund_net_value['直投累计收益'])/fund_net_value['直投金额(本金)'][0])**(365/fund_net_value['持有天数(直投)'])-1
    
    
        Stat_df = pd.DataFrame({
            '基金代码': code,
            '持有天数': fund_net_value['持有天数(直投)'].values[-1],
            '总购买份额' : '%.3f' % fund_net_value['直投累计购买份额(不变)'].values[0],
            '累计收益' : '%.3f' % fund_net_value['直投累计收益'].values[-1],
            '累计收益率' : '%.3f' % fund_net_value['直投累计收益率'].values[-1],
            '年化收益率' : '%.3f' % fund_net_value['直投累计年化收益率'].values[-1]
        }, index=['DIP'])
    
    if df:
        return fund_net_value
    else:
        return Stat_df
    
    
def AIP_Weekly_Plans(Freq, code, start_date, end_date, fund_category, fixed_investment, AIP=True, df=False):
    
    df = pd.DataFrame()
    
    for freq in Freq:
        df = df.append(AIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=fixed_investment, freq=freq, AIP=True, df=False))
        
    return df


def AIP_Weekly_plot(code, start_date, end_date, fund_category, fixed_investment=1000, Freq=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], figsize=(12,8)):
    
    fig,ax = plt.subplots(figsize=figsize)
    
    for freq in Freq:
        AIP_df = AIP_weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=fixed_investment, freq=freq, AIP=True, df=True)
    
        ax.plot(AIP_df.净值日期, AIP_df.累计收益率, label=freq)
        ax.legend()
    ax.set_xlabel("净值日期", fontsize=14)
    ax.set_ylabel("定投累计收益", fontsize=14)

    AIP_direct_df = AIP_weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=1000, freq='Monday', AIP=False, df=True)
    ax2=ax.twinx()
    ax2.plot(AIP_df.净值日期, AIP_direct_df["直投累计收益率"], '--', label='直投累计收益率')
    ax2.legend(loc='upper right')
    ax2.set_ylabel("直投累计收益率",fontsize=14)
    plt.show()

def Max_AIP_Weekly(code, start_date, end_date, fund_category, fixed_investment, Threshold=(-3.0, 2.0), AIP=True, df=False, Total_investment=100000):
    
    fund_net_value = get_fund_net_worth(code, start_date=start_date, end_date=end_date, fund_category=fund_category)
    
    fund_net_value['WeekDay'] = pd.to_datetime(fund_net_value['净值日期']).dt.day_name()
    
    if AIP:
        fund_net_value['定投金额(本金)'] = 0
        fund_net_value['累计定投金额(本金)'] = fund_net_value['定投金额(本金)'].cumsum()
            
        for i in range(len(fund_net_value['日增长率'])):
            if fund_net_value['日增长率'].values[i] <= Threshold[0]:
                fund_net_value['定投金额(本金)'][i] = fixed_investment
                fund_net_value['累计定投金额(本金)'] = fund_net_value['定投金额(本金)'].cumsum()
            elif (fund_net_value['日增长率'].values[i] >= Threshold[1]) & (fund_net_value['累计定投金额(本金)'].values[i-1] > fixed_investment):
                fund_net_value['定投金额(本金)'][i] = -fixed_investment
                fund_net_value['累计定投金额(本金)'] = fund_net_value['定投金额(本金)'].cumsum()
    
        fund_net_value['购买份额'] = fund_net_value['定投金额(本金)']/fund_net_value['单位净值']
        fund_net_value['累计份额'] = fund_net_value['购买份额'].cumsum()
        fund_net_value['平均成本'] = fund_net_value['累计定投金额(本金)']/fund_net_value['累计份额']
    
        fund_net_value['累计收益'] = (fund_net_value['单位净值'] - fund_net_value['平均成本']) * fund_net_value['累计份额']
        
        start_invest = fund_net_value['定投金额(本金)'].values.nonzero()[0][0]
        fund_net_value['持有天数'] = (fund_net_value['净值日期'] - fund_net_value['净值日期'][start_invest]).dt.days+1
        for i in range(len(fund_net_value['持有天数'])):
            if fund_net_value['持有天数'][i] < 0:
                fund_net_value['持有天数'][i] = 0
        fund_net_value['年化收益率'] = ((fund_net_value['累计收益'] + fund_net_value['累计定投金额(本金)'])/fund_net_value['累计定投金额(本金)'])**(365/fund_net_value['持有天数'])-1
    
        fund_net_value['累计收益率'] = fund_net_value['累计收益']/fund_net_value['累计定投金额(本金)']
        
        Stat_df = pd.DataFrame({
            '基金代码': code,
            '持有天数': fund_net_value['持有天数'].values[-1],
            '触发投资门槛(低买入)': Threshold[0],
            '触发投资门槛(高卖出)': Threshold[1],
            '单次金额': fixed_investment,
            '买入次数': len(fund_net_value[fund_net_value['定投金额(本金)'] == 1000]),
            '卖出次数': len(fund_net_value[fund_net_value['定投金额(本金)'] == -1000]),
            '总购买份额' : '%.3f' % fund_net_value['累计份额'].values[-1],
            '平均成本' : '%.3f' % fund_net_value['平均成本'].values[-1],
            '累计收益' : '%.3f' % fund_net_value['累计收益'].values[-1],
            '累计收益率' : '%.3f' % fund_net_value['累计收益率'].values[-1],
            '年化收益率' : '%.3f' % fund_net_value['年化收益率'].values[-1]
        }, index=['Plan'])
        
    else:
        
        fund_net_value['直投金额(本金)'] = 0
        fund_net_value['直投金额(本金)'][0] = Total_investment
        fund_net_value['直投累计购买份额(不变)'] = fund_net_value['直投金额(本金)'][0]/ fund_net_value['单位净值'][0]
        fund_net_value['直投累计收益'] = (fund_net_value['单位净值'] - fund_net_value['单位净值'][0]) * fund_net_value['直投金额(本金)'][0]
        fund_net_value['直投累计收益率'] = fund_net_value['直投累计收益']/fund_net_value['直投累计购买份额(不变)']
        fund_net_value['持有天数(直投)'] = (fund_net_value['净值日期'] - fund_net_value['净值日期'][0]).dt.days+1
        fund_net_value['直投累计年化收益率'] = ((fund_net_value['直投金额(本金)'][0] + fund_net_value['直投累计收益'])/fund_net_value['直投金额(本金)'][0])**(365/fund_net_value['持有天数(直投)'])-1
    
    
        Stat_df = pd.DataFrame({
            '基金代码': code,
            '持有天数': fund_net_value['持有天数(直投)'].values[-1],
            '总购买份额' : '%.3f' % fund_net_value['直投累计购买份额(不变)'].values[0],
            '累计收益' : '%.3f' % fund_net_value['直投累计收益'].values[-1],
            '累计收益率' : '%.3f' % fund_net_value['直投累计收益率'].values[-1],
            '年化收益率' : '%.3f' % fund_net_value['直投累计年化收益率'].values[-1]
        }, index=['DIP'])
    
    if df:
        return fund_net_value
    else:
        return Stat_df
    
    
def Max_AIP_Weekly_Plans(code, start_date, end_date, fund_category, fixed_investment, upper_threshold, lower_threshold):
    
    df = pd.DataFrame()
    threshold_list = list(itertools.product(lower_threshold, upper_threshold))
    for i in range(len(threshold_list)):

        df = df.append(Max_AIP_weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=fixed_investment, 
                       Threshold=threshold_list[i], df=False))
        
    return df

def AIP_Weekly_plot(code, start_date, end_date, fund_category, fixed_investment=1000, max_plan=max_plan, figsize=(12,8)):
    
    fig,ax = plt.subplots(figsize=figsize)
    
    for plan in max_plan:
        Max_AIP_df = Max_AIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=fixed_investment, 
                                    Threshold=max_plan[plan], AIP=True, df=True)
    
        ax.plot(Max_AIP_df.净值日期, Max_AIP_df.累计收益率, label=plan)
        ax.legend()
    ax.set_xlabel("净值日期", fontsize=14)
    ax.set_ylabel("定投累计收益", fontsize=14)

    Max_AIP_direct_df = Max_AIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=1000, AIP=False, df=True)
    ax2=ax.twinx()
    ax2.plot(Max_AIP_direct_df.净值日期, Max_AIP_direct_df["直投累计收益率"], 'r--', label='直投累计收益率')
    ax2.legend(loc='upper right')
    ax2.set_ylabel("直投累计收益率",fontsize=14)
    plt.show()


def StochasticAIP_Weekly(code, start_date, end_date, fund_category, fixed_investment, Freq, seed, df=False):
    
    fund_net_value = get_fund_net_worth(code, start_date=start_date, end_date=end_date, fund_category=fund_category)
    
    fund_net_value['WeekDay'] = pd.to_datetime(fund_net_value['净值日期']).dt.day_name()
    
    fund_net_value['定投金额(本金)'] = 0
    
    random.seed = seed
    final_day = list(range(0, len(AIP_df['WeekDay']), Freq))[-1]
    for i in list(range(0, final_day, Freq)):
        invest_date = random.choice(fund_net_value['WeekDay'][i:i+Freq].values)
        for j in range(i, i+Freq):
            if fund_net_value['WeekDay'].values[j] == invest_date:
                fund_net_value['定投金额(本金)'][j] = fixed_investment
                    
    fund_net_value['累计定投金额(本金)'] = fund_net_value['定投金额(本金)'].cumsum()
    fund_net_value['购买份额'] = fund_net_value['定投金额(本金)']/fund_net_value['单位净值']
    fund_net_value['累计份额'] = fund_net_value['购买份额'].cumsum()
    fund_net_value['平均成本'] = fund_net_value['累计定投金额(本金)']/fund_net_value['累计份额']

    fund_net_value['累计收益'] = (fund_net_value['单位净值'] - fund_net_value['平均成本']) * fund_net_value['累计份额']
    
    start_invest = fund_net_value['定投金额(本金)'].values.nonzero()[0][0]
    fund_net_value['持有天数'] = (fund_net_value['净值日期'] - fund_net_value['净值日期'][start_invest]).dt.days+1
    for i in range(len(fund_net_value['持有天数'])):
        if fund_net_value['持有天数'][i] < 0:
            fund_net_value['持有天数'][i] = 0
    fund_net_value['年化收益率'] = ((fund_net_value['累计收益'] + fund_net_value['累计定投金额(本金)'])/fund_net_value['累计定投金额(本金)'])**(365/fund_net_value['持有天数'])-1

    fund_net_value['累计收益率'] = fund_net_value['累计收益']/fund_net_value['累计定投金额(本金)']
    
    Stat_df = pd.DataFrame({
        '基金代码': code,
        '持有天数': fund_net_value['持有天数'].values[-1],
        '定投时间': '随机',
        '定投金额': fixed_investment,
        '分投期数': fund_net_value['累计定投金额(本金)'].values[-1]/fixed_investment,
        '总购买份额' : '%.3f' % fund_net_value['累计份额'].values[-1],
        '平均成本' : '%.3f' % fund_net_value['平均成本'].values[-1],
        '累计收益' : '%.3f' % fund_net_value['累计收益'].values[-1],
        '累计收益率' : '%.3f' % fund_net_value['累计收益率'].values[-1],
        '年化收益率' : '%.3f' % fund_net_value['年化收益率'].values[-1]
    }, index=['Plan'])
    
    if df:
        return fund_net_value
    else:
        return Stat_df
    

def StochasticAIP_Weekly_Plans(Freq, seed, code, start_date, end_date, fund_category, fixed_investment):
    
    df = pd.DataFrame()
    
    for seed in seed:
        df = df.append(StochasticAIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, 
                                            fixed_investment=fixed_investment, Freq=Freq, seed=seed, df=False))
        
    return df

