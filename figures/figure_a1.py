import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def figure_a1():
    '''
    This function creates Figure A1 in the Internet Appendix. 
    '''

    df = pd.read_csv('../../data/pi_horizons.csv')

    df = df.dropna()
    df = df.reset_index(drop=True)

    sns.set_style('darkgrid')
    sns.set_palette(palette = 'tab20', n_colors = 20)
    plt.rc('axes', titlesize=14)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
    plt.rc('legend', fontsize=12)    # legend fontsize
    plt.rc('font', size=12)          # controls default text sizes

    fig, ax = plt.subplots(figsize=(12, 9), tight_layout=True)

    colors = [
        '#003f5c', 
        '#7a5195',
        '#ef5675', 
        '#ffa600',
    ]

    count = 0
    for variable in df.columns[1:]:
        ax.plot(df['time'], df[variable], label = variable, color=colors[count])
        count+=1

    # Label axis
    ax.set(
        xlabel='Time, seconds',
        ylabel="Price Impact, % of total"
        )

    ax.legend()

    # Export the graph
    fig.savefig(
    '../../data/graphs/pi_horizons.png')
    plt.close(fig)

if __name__ == "__main__":
    figure_a1()
