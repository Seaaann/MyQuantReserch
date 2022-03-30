import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import akshare as ak


def volatility_rank(df, PLOT=True):

    ts = df['close'].pct_change().dropna()
    monthly_annualized_volatility = ts.resample('M').std() * np.sqrt(12)
    ranked = monthly_annualized_volatility.groupby(
        monthly_annualized_volatility.index.year).rank()
    final = ranked.groupby(ranked.index.month).mean()

    if PLOT:
        max_volatility_month = final[final == final.max()].index[0]
        min_volatility_month = final[final == final.min()].index[0]
        b_plot = plt.bar(x=final.index, height=final)
        b_plot[max_volatility_month - 1].set_color('g')
        b_plot[min_volatility_month - 1].set_color('r')
        for i, v in enumerate(round(final, 2)):
            plt.text(i + .8, 1, str(v), color='black', fontweight='bold')
        plt.axhline(final.mean(),
                    ls='--',
                    color='k',
                    label=round(final.mean(), 2))
        plt.title('Average Monthly Volatility Ranking since {}'.format(
            df.index.year[0]))

        plt.legend()
        plt.show()
    return final


def AMVR(df):

    final = volatility_rank(df, PLOT=False)
    final.rename(index={
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    },
                 inplace=True)
    AMVR = abs(final - final.mean())

    return AMVR.sort_values()