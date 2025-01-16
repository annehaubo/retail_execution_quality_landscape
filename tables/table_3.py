import pandas as pd
import numpy as np
from scipy import signal

def changes_in_routing():
    '''
    This function calculates the average absolute change 
    in routing for each broker wholesaler across months.
    It also calculates the high low routing changes.
    These results are presented in Table 3 in the paper and Table A1 in the Internet Appendix.
    '''

    df = pd.read_csv('../../data/606_data.csv', parse_dates=['Year Month'])

    # Extract just the brokers and wholesalers in our sample
    wholesalers = [
        'Citadel Securities, LLC',
        'Virtu Americas, LLC',
        'G1 Execution Services, LLC',
        'Jane Street Capital, LLC',
        'Two Sigma Securities, LLC',
        'UBS Securities, LLC',
        'Bank of America Merrill Lynch',
        'Morgan Stanley & Co., LLC',
    ]
    df = df[df['Route firm display'].isin(wholesalers) == True]
    df = df.reset_index(drop=True)

    brokers = [
        'Charles Schwab',
        'E*TRADE Securities, LLC',
        'Merrill Lynch Pierce Fenner & Smith Inc.',
        'Morgan Stanley Wealth Management',
        'Robinhood Securities LLC',
        'TD Ameritrade Clearing, Inc.',
        'TD Ameritrade, Inc.',
        'Tradestation Securities',
        'View Trade',
        'Webull Financial LLC',
    ]  

    df = df[df['Entry firm display'].isin(brokers) == True]
    df = df.reset_index(drop=True)

    df['mkt_mktbl_shares'] = df['Estimated Market Shares'] + df['Estimated Marketable Limit Shares']

    # Only keep data for 2020-2022
    df = df[df['Year Month'] < '2023-01-01']
    df = df.reset_index(drop=True)

    # Market share of each broker across all brokers
    group1 = df.groupby(by=['Entry firm display', 'Year Month'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()

    # Sum across S&P500 and Other stocks
    group1 = df.groupby(by=['Route firm display', 'Entry firm display', 'Year Month'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()
    del group1

    # Calculate the market share
    group = df1.groupby(by=['Entry firm display', 'Year Month'])

    total_shares = group.agg({
        'mkt_mktbl_shares': 'sum'
    })
    total_shares = total_shares.reset_index()
    total_shares.columns=['Entry firm display', 'Year Month', 'mkt_mktbl_shares_total']
    del group

    df1 = df1.merge(total_shares, on=['Entry firm display', 'Year Month'])

    df1['mkt_mktbl_share_prop'] = ((df1['mkt_mktbl_shares'] / df1['mkt_mktbl_shares_total'])) * 100

    # Do a pivot table across year month so we incert zeros for months where we have no routing to a specific wholesaler
    df_pivot1 = df1.pivot_table(index=['Entry firm display', 'Year Month'], columns=['Route firm display'], values=['mkt_mktbl_share_prop'], fill_value=0)
    df_pivot1 = df_pivot1.reset_index()
    columns = [
        'Entry firm display', 
        'Year Month',
        'Bank of America Merrill Lynch',
        'Citadel Securities, LLC',
        'G1 Execution Services, LLC',
        'Jane Street Capital, LLC',
        'Morgan Stanley & Co., LLC',
        'Two Sigma Securities, LLC',
        'UBS Securities, LLC',
        'Virtu Americas, LLC',
    ]
    df_pivot1.columns = columns
    del columns

    # # Calculate the change
    for wholesaler in wholesalers:

        df_pivot1[f'{wholesaler} lag'] = np.where(
            (df_pivot1['Entry firm display'] == df_pivot1['Entry firm display'].shift(1)),
            df_pivot1[wholesaler].shift(1),
            np.nan
        )

        df_pivot1[f'{wholesaler} abs_change'] = (df_pivot1[wholesaler] - df_pivot1[f'{wholesaler} lag']).abs()

        # Calcualte the start and finish market shares
        df_pivot1[f'{wholesaler}_start'] = np.where(
            (df_pivot1['Year Month'] == '2020-01-01'),
            df_pivot1[wholesaler],
            np.nan
        )
        df_pivot1[f'{wholesaler}_start'] = np.where(
                ((df_pivot1['Entry firm display'] == 'Merrill Lynch Pierce Fenner & Smith Inc.') & (df_pivot1['Year Month'] == '2021-07-01')),
                df_pivot1[wholesaler],
                df_pivot1[f'{wholesaler}_start']
            )

        df_pivot1[f'{wholesaler}_end'] = np.where(
            (df_pivot1['Year Month'] == '2022-12-01'),
            df_pivot1[wholesaler],
            np.nan
        )

    # Calculate the average change by broker and wholesaler across months
    group = df_pivot1.groupby(by=['Entry firm display'])
    stats = group.agg({
        'Citadel Securities, LLC abs_change': 'mean',
        'Citadel Securities, LLC_start': 'mean',
        'Citadel Securities, LLC_end': 'mean',
        'Virtu Americas, LLC abs_change': 'mean',
        'Virtu Americas, LLC_start': 'mean',
        'Virtu Americas, LLC_end': 'mean',
        'G1 Execution Services, LLC abs_change': 'mean',
        'G1 Execution Services, LLC_start': 'mean',
        'G1 Execution Services, LLC_end': 'mean',
        'Jane Street Capital, LLC abs_change': 'mean',
        'Jane Street Capital, LLC_start': 'mean',
        'Jane Street Capital, LLC_end': 'mean',
        'Two Sigma Securities, LLC abs_change': 'mean',
        'Two Sigma Securities, LLC_start': 'mean',
        'Two Sigma Securities, LLC_end': 'mean',
        'UBS Securities, LLC abs_change': 'mean',
        'UBS Securities, LLC_start': 'mean',
        'UBS Securities, LLC_end': 'mean',
        'Bank of America Merrill Lynch abs_change': 'mean',
        'Bank of America Merrill Lynch_start': 'mean',
        'Bank of America Merrill Lynch_end': 'mean',
        'Morgan Stanley & Co., LLC abs_change': 'mean',
        'Morgan Stanley & Co., LLC_start': 'mean',
        'Morgan Stanley & Co., LLC_end': 'mean',
    })
    stats = stats.reset_index()

    for wholesaler in wholesalers:
        stats[f'{wholesaler} start finish'] = "'" +   stats[f'{wholesaler}_start'].round().astype(int).astype(str) + '-' + stats[f'{wholesaler}_end'].round().astype(int).astype(str)

    stats = stats.drop(columns=[
        'Citadel Securities, LLC_start',
        'Citadel Securities, LLC_end',
        'Virtu Americas, LLC_start',
        'Virtu Americas, LLC_end',
        'G1 Execution Services, LLC_start',
        'G1 Execution Services, LLC_end',
        'Jane Street Capital, LLC_start',
        'Jane Street Capital, LLC_end',
        'Two Sigma Securities, LLC_start',
        'Two Sigma Securities, LLC_end',
        'UBS Securities, LLC_start',
        'UBS Securities, LLC_end',
        'Bank of America Merrill Lynch_start',
        'Bank of America Merrill Lynch_end',
        'Morgan Stanley & Co., LLC_start',
        'Morgan Stanley & Co., LLC_end',
    ])

    # Order the rows for easier formatting
    # Define the desired order
    desired_order = [
        'TD Ameritrade Clearing, Inc.',
        'TD Ameritrade, Inc.',
        'Robinhood Securities LLC',
        'Charles Schwab',
        'E*TRADE Securities, LLC',
        'View Trade',
        'Webull Financial LLC',
        'Tradestation Securities',
        'Merrill Lynch Pierce Fenner & Smith Inc.',
        'Morgan Stanley Wealth Management',
        ''
        ]

    # Convert 'Entry firm display' column to a categorical type with the desired order
    stats['Entry firm display'] = pd.Categorical(stats['Entry firm display'], categories=desired_order, ordered=True)

    stats = stats.sort_values('Entry firm display')

    # Calculate the high lows
    stats2 = group.agg({
        'Citadel Securities, LLC': ['min', 'max'],
        'Virtu Americas, LLC': ['min', 'max'],
        'G1 Execution Services, LLC': ['min', 'max'],
        'Jane Street Capital, LLC': ['min', 'max'],
        'Two Sigma Securities, LLC': ['min', 'max'],
        'UBS Securities, LLC': ['min', 'max'],
        'Bank of America Merrill Lynch': ['min', 'max'],
        'Morgan Stanley & Co., LLC': ['min', 'max'],
        
    })
    stats2 = stats2.reset_index()

    columns = [
        'Entry firm display',
        'Citadel Securities, LLC Min',
        'Citadel Securities, LLC Max',
        'Virtu Americas, LLC Min',
        'Virtu Americas, LLC Max',
        'G1 Execution Services, LLC Min',
        'G1 Execution Services, LLC Max',
        'Jane Street Capital, LLC Min',
        'Jane Street Capital, LLC Max',
        'Two Sigma Securities, LLC Min',
        'Two Sigma Securities, LLC Max',
        'UBS Securities, LLC Min',
        'UBS Securities, LLC Max',
        'Bank of America Merrill Lynch Min',
        'Bank of America Merrill Lynch Max',
        'Morgan Stanley & Co., LLC Min',
        'Morgan Stanley & Co., LLC Max',
        
    ]
    stats2.columns = columns

    # Create a high low variable
    for wholesaler in wholesalers:
        stats2[f'{wholesaler} Low High'] = "'" +   stats2[f'{wholesaler} Min'].round().astype(int).astype(str) + '-' + stats2[f'{wholesaler} Max'].round().astype(int).astype(str)

    # Convert 'Entry firm display' column to a categorical type with the desired order
    stats2['Entry firm display'] = pd.Categorical(stats2['Entry firm display'], categories=desired_order, ordered=True)

    stats2 = stats2.sort_values('Entry firm display')

    stats2 = stats2.drop(columns=columns[1:])

    stats = pd.concat([stats, stats2])

    stats.to_csv('../../data/table_3.csv', index=False)

    # We then format Table 3 in the paper using the absolute change.
    # Table A1 in the appendix expands on Table 3 by reporting the 
    # smallest to largest and beginning to end routing statistics 
    # alongside the absolute change. This formatting is done in excel.

if __name__ == "__main__":
    changes_in_routing()