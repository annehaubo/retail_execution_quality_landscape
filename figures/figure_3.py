import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def figure_3():
    '''
    This function creates a bar graph of the adjusted coefficients from running
    ../panels/606_regs.do. We adjust the coefficients to make them interpretable as described in the paper.
    The lines are 95% confidence intervals extracted directly from Stata. 
    The function creates Figure 3 in the paper.
    '''

    # Sample data
    categories = [
        'TD Ameritrade',
        'TradeStation',
        'Schwab',
        'E*TRADE',
        'Webull',
        'TD Clearing',
        'Robinhood',
        'Merril Lynch',
        'ViewTrade',
        'Morgan Stanley',
    ]
    values = [
        2.31,
        0.91,
        0.56,
        0.14,
        0.00,
        0.00,
        -0.42,
        -0.55,
        -0.90,
        -1.99,
    ]

    # Start and end points for the lines for the 95% CI
    line_starts =[
        2.033973803,
        0.518796276,
        0.2926096,
        -0.076023196,
        -0.201052901,
        -0.160037322,
        -0.102631481,
        -0.722926038,
        -1.150450233,
        -2.233155132,
    ]

    line_ends = [
        2.603034536,
        1.239704387,
        0.852650514,
        0.363292122,
        0.191234778,
        0.114622075,
        -0.678951706,
        -0.316412181,
        -0.683488001,
        -1.765894504,
    ]

    # Calculating the positions of the bars
    x_pos = np.arange(len(categories))

    sns.set_style('darkgrid')
    sns.set_palette(palette = 'tab20', n_colors = 20)
    plt.rc('axes', titlesize=14)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
    plt.rc('legend', fontsize=12)    # legend fontsize
    plt.rc('font', size=12)          # controls default text sizes

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(12, 9), tight_layout=True)
    bars = ax.bar(x_pos, values, color='#003f5c', label='Values')

    # Adding a vertical line through each bar
    for bar, start, end in zip(bars, line_starts, line_ends):
        plt.vlines(x=bar.get_x() + bar.get_width() / 2, ymin=start, ymax=end, colors='#bc5090', linestyles='solid')

    ax.set_ylim(-3,3)

    # Adding some labels and a title
    plt.xticks(x_pos, categories, rotation=45, ha="right")
    plt.ylabel('Price Impact (%)')

    # Export the graph
    fig.savefig('../../data/graphs/figure_3.png')
    plt.close(fig)

if __name__ == "__main__":
    figure_3()