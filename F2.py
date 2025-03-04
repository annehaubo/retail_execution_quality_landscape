import pandas as pd
import numpy as np

def sankey_data():
    '''
    This function creates the data for the sankey matic graph (Figure 2 in the paper).
    The data should then be inputted into https://sankeymatic.com/build/ to create the figure.
    '''

    df = pd.read_csv('../../data/606_data.csv', parse_dates=['date'])
    print(df.dtypes)

    # Sum the market and marketable shares
    df['Estimated Market and Marketable Shares'] = df['mkt_shares'] + df['mktbl_shares']

    # Insert missing months so when a broker does not route to a wholesaler
    # it shows up as zero.
    min_date = df['date'].min()
    max_date = df['date'].max()
    all_months = pd.date_range(start=min_date, end=max_date, freq='MS')

    # Generate all possible combinations of 'broker', 'market_center' and 'date'
    df_full = pd.MultiIndex.from_product(
        [df['broker'].unique(), df['market_center'].unique(), all_months],
        names=['broker', 'market_center', 'date']
    ).to_frame(index=False)

    # Merge this with original data
    df_full = df_full.merge(df, on=['broker', 'market_center', 'date'], how='left')

    # Fill missing 'Estimated Market and Marketable Shares' with zero
    df_full['Estimated Market and Marketable Shares'] = df_full['Estimated Market and Marketable Shares'].fillna(0)
    del df
    del min_date
    del max_date
    del all_months

    # Sum the volume across S&P500 and Other Stocks
    broker_venue_group = df_full.groupby(by=['broker', 'market_center', 'date'])

    stats_all_stocks = broker_venue_group.agg({
        'Estimated Market and Marketable Shares': 'sum',
    })
    stats_all_stocks = stats_all_stocks.reset_index()

    # Sum the estimated shares from each broker to each route venue
    stats_group = stats_all_stocks.groupby(by=['broker', 'market_center'])
    stats = stats_group.agg({
        'Estimated Market and Marketable Shares': 'mean',
    })
    stats = stats.reset_index()
    stats.columns = [
        'broker', 
        'market_center',
        'Estimated Market and Marketable Shares',
    ]

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
            stats['broker'] + ' [' + stats[variable].astype('str') + '] ' + stats['market_center'],
            np.nan
            )

    # Sum the total and monthly average to rank the flows in the graph

    rank_group = stats.groupby(by=['broker'])
    rank = rank_group.agg({
        'Estimated Market and Marketable Shares': 'sum',
    })
    rank = rank.reset_index()
    rank.columns = [
        'broker', 
        'Rank Total Estimated Market and Marketable Shares',
    ]

    stats = stats.merge(rank, on='broker', how='left')

    rank_group = stats.groupby(by=['market_center'])
    rank = rank_group.agg({
        'Estimated Market and Marketable Shares': 'sum',
    })
    rank = rank.reset_index()
    rank.columns = [
        'market_center', 
        'Route Rank Total Estimated Market and Marketable Shares',
    ]

    stats = stats.merge(rank, on='market_center', how='left')

    stats.to_csv('../../data/graphs/sankey_data.csv', index=False)


if __name__ == "__main__":
    sankey_data()
