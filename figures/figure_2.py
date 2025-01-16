import pandas as pd
import numpy as np 

# Don't use the average statistics produced here. When there are no flows to a wholesaler or exchange 
# it shows up as missing and not zero so the averaging is not done across all 48 months for 
# ever wholesaler/exchange. Use the totals instead. 

def sankey_data():
    '''
    This function creates the data for the sankey matic graph (Figure 2 in the paper).
    The data should then be inputted into https://sankeymatic.com/build/ to create the figure.
    '''

    df = pd.read_csv('../../data/606_data.csv', parse_dates=['Year Month'])
    print(df.dtypes)

    # Sum the market and marketable shares
    df['Estimated Market and Marketable Shares'] = df['Estimated Market Shares'] + df['Estimated Marketable Limit Shares']

    # Insert missing months so when a broker does not route to a wholesaler
    # it shows up as zero.
    min_date = df['Year Month'].min()
    max_date = df['Year Month'].max()
    all_months = pd.date_range(start=min_date, end=max_date, freq='MS')

    # Generate all possible combinations of 'Entry firm display', 'Route firm display' and 'Year Month'
    df_full = pd.MultiIndex.from_product(
        [df['Entry firm display'].unique(), df['Route firm display'].unique(), all_months],
        names=['Entry firm display', 'Route firm display', 'Year Month']
    ).to_frame(index=False)

    # Merge this with original data
    df_full = df_full.merge(df, on=['Entry firm display', 'Route firm display', 'Year Month'], how='left')

    # Fill missing 'Estimated Market and Marketable Shares' with zero
    df_full['Estimated Market and Marketable Shares'] = df_full['Estimated Market and Marketable Shares'].fillna(0)
    del df
    del min_date
    del max_date
    del all_months

    # Sum the volume across S&P500 and Other Stocks
    broker_venue_group = df_full.groupby(by=['Entry firm display', 'Route firm display', 'Year Month'])

    stats_all_stocks = broker_venue_group.agg({
        'Estimated Market and Marketable Shares': 'sum',
    })
    stats_all_stocks = stats_all_stocks.reset_index()

    # Sum the estimated shares from each broker to each route venue
    stats_group = stats_all_stocks.groupby(by=['Entry firm display', 'Route firm display'])
    stats = stats_group.agg({
        'Estimated Market and Marketable Shares': 'mean',
    })
    stats = stats.reset_index()
    stats.columns = [
        'Entry firm display', 
        'Route firm display',
        'Estimated Market and Marketable Shares',
    ]

    # Format broker and wholesaler labels
    renames = [
        ['Charles Schwab', 'Schwab'],
        ['E*TRADE Securities, LLC', 'E*TRADE'],
        ['Robinhood Securities LLC', 'Robinhood'],
        ['TD Ameritrade Clearing, Inc.', 'TD Clearing'],
        ['TD Ameritrade, Inc.', 'TD Ameritrade'],
        ['Tradestation Securities', 'TradeStation'],
        ['View Trade', 'ViewTrade'],
        ['Webull Financial LLC', 'Webull'],
        ['Merrill Lynch Pierce Fenner & Smith Inc.', 'Merrill Lynch.'],
        ['Morgan Stanley Wealth Management', 'Morgan Stanley.'],
        ['Citadel Securities, LLC', 'Citadel'],
        ['G1 Execution Services, LLC', 'G1'],
        ['Jane Street Capital, LLC', 'Jane Street'],
        ['Two Sigma Securities, LLC', 'Two Sigma'],
        ['UBS Securities, LLC', 'UBS'],
        ['Virtu Americas, LLC', 'Virtu'],
        ['Bank of America Merrill Lynch', 'Merrill Lynch'],
        ['Morgan Stanley & Co., LLC', 'Morgan Stanley'],
    ]

    for rename in renames[:10]:
        stats['Entry firm display'] = np.where(
            (stats['Entry firm display'] == rename[0]),
            rename[1],
            stats['Entry firm display']
        )

    for rename in renames[10:]:
        stats['Route firm display'] = np.where(
            (stats['Route firm display'] == rename[0]),
            rename[1],
            stats['Route firm display']
        )


    # Rebase shares in millions
    stats['Estimated Market and Marketable Shares'] = (stats['Estimated Market and Marketable Shares'] / 1000000).round(decimals=0)

    # Save as integer for graphing
    stats['Estimated Market and Marketable Shares'] = stats['Estimated Market and Marketable Shares'].astype('int')

    # Create formatted variables
    variables = [
        'Estimated Market and Marketable Shares',
    ]
    for variable in variables:
        stats[f'{variable} formatted'] = np.where(
            (stats[variable] > 0),
            stats['Entry firm display'] + ' [' + stats[variable].astype('str') + '] ' + stats['Route firm display'],
            np.nan
            )

    # Sum the total and monthly average to rank the flows in the graph

    rank_group = stats.groupby(by=['Entry firm display'])
    rank = rank_group.agg({
        'Estimated Market and Marketable Shares': 'sum',
    })
    rank = rank.reset_index()
    rank.columns = [
        'Entry firm display', 
        'Rank Total Estimated Market and Marketable Shares',
    ]

    stats = stats.merge(rank, on='Entry firm display', how='left')

    rank_group = stats.groupby(by=['Route firm display'])
    rank = rank_group.agg({
        'Estimated Market and Marketable Shares': 'sum',
    })
    rank = rank.reset_index()
    rank.columns = [
        'Route firm display', 
        'Route Rank Total Estimated Market and Marketable Shares',
    ]

    stats = stats.merge(rank, on='Route firm display', how='left')

    stats.to_csv('../../data/graphs/sankey_data.csv', index=False)


if __name__ == "__main__":
    sankey_data()
