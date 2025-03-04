import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

def figure_4():
    '''
    This function graphs the market share over time for Jane Street and the pre 
    and post period used in the regression estimation in Table 8. The function creates 
    Figure 4 in the paper. The inputs to the figure is made by running the appropriate code in ./F1, F4, T1, T4.sas.
    '''

    # import data
    df = pd.read_csv('../../data/input_data.csv', parse_dates=['date'])

    # format date
    df['Year Month'] = pd.to_datetime(df['date'], format='%Y%m')

    # Rabase the market share stats to percent
    df['jane_market_share'] = df['jane_market_share'] * 100

    # Set the dates to the 15th of every month so the shaded areas are more correct
    df['Year Month'] = df['Year Month'].apply(lambda x: x.replace(day=15))

    sns.set_style('dark')
    sns.set_palette(palette = 'tab20', n_colors = 20)
    plt.rc('axes', titlesize=14)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)     # fontsize of the x and y labels
    plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
    plt.rc('legend', fontsize=12)    # legend fontsize
    plt.rc('font', size=12)          # controls default text sizes

    fig, ax = plt.subplots(figsize=(12, 9), tight_layout=True)

    ax.stackplot(df['Year Month'], df['jane_market_share'], color = '#003f5c')

    ax.set(
            xlabel='Year Month',
            ylabel='Market Share (%)'
            )
    
    ax.set_xlim(datetime.datetime(2019, 1, 1), datetime.datetime(2023, 1, 1))

    # Add shaded areas for our pre and post period
    ax.axvspan(pd.Timestamp(2021, 4, 15), pd.Timestamp(2021, 6, 15), color='#7a5195', alpha=0.5)
    ax.axvspan(pd.Timestamp(2021, 10, 15), pd.Timestamp(2021, 12, 15), color='#7a5195', alpha=0.5)

    # Export the graph
    fig.savefig(
    '../../data/graphs/figure_4.png')
    plt.close(fig)

if __name__ == "__main__":
    figure_4()