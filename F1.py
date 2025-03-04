import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def figure_1():
    '''
    This function creates a scatterplot of the hhi measure by stock which is Figure 1 in the paper.
    The inputs to the figure is made by running the appropriate code in ./F1, F4, T1, T4.sas.
    '''

    df = pd.read_csv('../../data/input_data.csv')
    print(df.dtypes)

    # Round the hhi
    df['hhi'] = df['hhi'].round(0)
    df['hhi'] = df['hhi'].astype('int')

    df = df.reset_index()

    sns.set_style('darkgrid')
    sns.set_palette(palette  = 'tab20', n_colors = 20)
    plt.rc('axes', titlesize=14)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)     # fontsize of the x and y labels
    plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
    plt.rc('legend', fontsize=12)    # legend fontsize
    plt.rc('font', size=12)          # controls default text sizes

    fig, ax = plt.subplots(figsize=(12, 9), tight_layout=True)

    ax.scatter(df['index'], df['hhi'], s=10, color = '#003f5c', label='Individual Stock HHI')
    # Label axis
    ax.set(
        xlabel='Stocks',
        ylabel='HHI'
        )

    ax.hlines(2500, color='#bc5090', xmin=0, xmax=12012, label='High Concentration')
    ax.hlines(1500, color='#ffa600', xmin=0, xmax=12012, label='Moderate Concentration')

    ax.legend()

    ax.set_xlim(0, 12012)
    ax.set_ylim(0, 10000)

    fig.savefig(
        '../../data/graphs/figure_1.png')
    plt.close(fig)

if __name__ == "__main__":
    figure_1()
