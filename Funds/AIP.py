from fund_tools import *
import random



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
        AIP_df = AIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=fixed_investment, freq=freq, AIP=True, df=True)

        ax.plot(AIP_df.净值日期, AIP_df.累计收益率, label=freq)
        ax.legend()
    ax.set_xlabel("净值日期", fontsize=14)
    ax.set_ylabel("定投累计收益", fontsize=14)

    AIP_direct_df = AIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=1000, freq='Monday', AIP=False, df=True)
    ax2=ax.twinx()
    ax2.plot(AIP_direct_df.净值日期, AIP_direct_df["直投累计收益率"], '--', label='直投累计收益率')
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

        df = df.append(Max_AIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=fixed_investment,
                       Threshold=threshold_list[i], df=False))

    return df

def Max_AIP_Weekly_plot(code, start_date, end_date, fund_category, fixed_investment=1000, max_plan={'plan 1': (-1.0, 1.0),
                                                                                                    'plan 2': (-2.0, 2.0),
                                                                                                    'plan 3': (-3.0, 3.0),
                                                                                                    'plan 4': (-3.0, 2.0),
                                                                                                    'plan 5': (-3.0, 1.0)}, figsize=(12,8)):

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


def StochasticAIP_Weekly(code, start_date, end_date, fund_category, fixed_investment, Freq, seed, df=False, AIP=True, Total_investment=100000):

    fund_net_value = get_fund_net_worth(code, start_date=start_date, end_date=end_date, fund_category=fund_category)

    fund_net_value['WeekDay'] = pd.to_datetime(fund_net_value['净值日期']).dt.day_name()

    if AIP:
        fund_net_value['定投金额(本金)'] = 0

        random.seed = seed
        final_day = list(range(0, len(fund_net_value['WeekDay']), Freq))[-1]
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


def StochasticAIP_Weekly_Plans(Freq, seed, code, start_date, end_date, fund_category, fixed_investment):

    df = pd.DataFrame()

    for seed in seed:
        df = df.append(StochasticAIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category,
                                            fixed_investment=fixed_investment, Freq=Freq, seed=seed, df=False, AIP=True))

    return df


def StochasticAIP_Weekly_plot(code, start_date, end_date, fund_category, fixed_investment=1000, Seed=[1,2,3,4,5], figsize=(12,8)):

    fig,ax = plt.subplots(figsize=figsize)

    for s in Seed:
        stochasticAIP_df = StochasticAIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=fixed_investment,
                                                Freq=5, seed=s, AIP=True, df=True)

        ax.plot(stochasticAIP_df.净值日期, stochasticAIP_df.累计收益率, label='Seed '+ str(s))
        ax.legend()
    ax.set_xlabel("净值日期", fontsize=14)
    ax.set_ylabel("定投累计收益", fontsize=14)

    stochasticAIP_direct_df = StochasticAIP_Weekly(code, start_date=start_date, end_date=end_date, fund_category=fund_category, fixed_investment=1000,
                                                   Freq=5, seed=123, AIP=False, df=True)
    ax2=ax.twinx()
    ax2.plot(stochasticAIP_direct_df.净值日期, stochasticAIP_direct_df["直投累计收益率"], 'r--', label='直投累计收益率')
    ax2.legend(loc='upper right')
    ax2.set_ylabel("直投累计收益率",fontsize=14)
    plt.show()



