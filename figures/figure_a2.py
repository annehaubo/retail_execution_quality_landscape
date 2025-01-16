import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import datetime

def figure_a2():
    '''
    This function graphs the parallel trends of realized spreads for 
    wholesalers and exchanges which is Internet Appendix Figure A2 in the paper.
    '''

    df = pd.read_csv('../../data/rs_whol_exch.csv')

    df['Year Month'] = pd.to_datetime(df['date'], format='%Y%m')

    sns.set_style('darkgrid')
    sns.set_palette(palette = 'tab20', n_colors = 20)
    plt.rc('axes', titlesize=14)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)     # fontsize of the x and y labels
    plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
    plt.rc('legend', fontsize=12)    # legend fontsize
    plt.rc('font', size=12)          # controls default text sizes

    fig, (ax, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 9), tight_layout=True)

    ax.plot(df['Year Month'], df['whol'], label='Wholesalers', color='#003f5c')
    ax.plot(df['Year Month'], df['exch'], label='Exchanges', color='#bc5090')

    ax2.plot(df['Year Month'], df['whol'], label='Wholesalers', color='#003f5c')
    ax2.plot(df['Year Month'], df['exch'], label='Exchanges', color='#bc5090')

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
        ylabel='Realized Spread (bps)'
    )

    ax2.set(
        xlabel='Post'
    )

    ax.legend(loc='upper left')

    # Export the graph
    fig.savefig('../../data/graphs/figure_a2.png')
    plt.close(fig)

if __name__ == "__main__":
    figure_a2()