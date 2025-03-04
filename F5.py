import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

def figure_5():
    '''
    This function creates a graph of the fitted values of Jane and the Incumbents 
    from Table 8 and produces Figure 5.
    '''

    df = pd.read_csv('../../data/input_data.csv')

    df['Year Month'] = pd.to_datetime(df['date'], format='%b-%y')
    df = df.drop(columns=['date'])

    sns.set_style('darkgrid')
    sns.set_palette(palette = 'tab20', n_colors = 20)
    plt.rc('axes', titlesize=14)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
    plt.rc('legend', fontsize=12)    # legend fontsize
    plt.rc('font', size=12)          # controls default text sizes

    # Graph only Jane and the incumbants
    fig, (ax, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 9), tight_layout=True)


    ax.plot(df['Year Month'], df['Incumbents_mean'], label='Incumbents', color='#003f5c')
    ax2.plot(df['Year Month'], df['Incumbents_mean'], label='Incumbents', color='#003f5c')

    ax.plot(df['Year Month'], df['Jane_mean'], label="Jane Street", color='#bc5090')
    ax2.plot(df['Year Month'], df['Jane_mean'], label="Jane Street", color='#bc5090')

    # Add shaded aread between the confidence intervals
    ax.fill_between(df['Year Month'], df['Incumbents_CI 10'], df['Incumbents_CI 90'], color='#003f5c', alpha=0.25)
    ax2.fill_between(df['Year Month'], df['Incumbents_CI 10'], df['Incumbents_CI 90'], color='#003f5c', alpha=0.25)

    ax.fill_between(df['Year Month'], df['Jane_CI 10'], df['Jane_CI 90'], color='#bc5090', alpha=0.5)
    ax2.fill_between(df['Year Month'], df['Jane_CI 10'], df['Jane_CI 90'], color='#bc5090', alpha=0.5)


    ax.set_xlim(datetime.datetime(2021, 4, 1), datetime.datetime(2021, 6, 1))
    ax2.set_xlim(datetime.datetime(2021, 10, 1), datetime.datetime(2021, 12, 1))

    # Format the ticks to show the month and year only
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # Use diagonal lines to indicate that the axis is broken
    d = .008  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)
    #ax.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs) #This is the break for the top axis

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    #ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs) #This is the break for the top axis
    ax2.plot((-d, +d), (-d, +d), **kwargs)

    # Label axis
    ax.set(
        xlabel='Pre',
        ylabel='Fitted Values'
    )

    ax2.set(
        xlabel='Post'
    )

    ax2.set_ylim(0, 25)

    ax.legend(loc='upper left')

    # Export the graph
    fig.savefig(
    '../../data/graphs/figure_5.png')
    plt.close(fig)

if __name__ == "__main__":
    figure_5()
