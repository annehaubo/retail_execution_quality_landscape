import pandas as pd

def table_2():
    '''
    This function calculates the average broker market share and 
    the average wholesaler market share for each broker. 
    These results are presented in Table 2 in the paper.
    '''

    df = pd.read_csv('../../data/606_data.csv', parse_dates=['Year Month'])

    # Extract just the brokers and wholesalers in our sample
    wholesalers = [
        'Bank of America Merrill Lynch',
        'Citadel Securities, LLC',
        'G1 Execution Services, LLC',
        'Jane Street Capital, LLC',
        'Morgan Stanley & Co., LLC',
        'Two Sigma Securities, LLC',
        'UBS Securities, LLC',
        'Virtu Americas, LLC',
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

    # Only keep data for 2020-2022
    df = df[df['Year Month'] < '2023-01-01']
    df = df.reset_index(drop=True)

    df['mkt_mktbl_shares'] = df['Estimated Market Shares'] + df['Estimated Marketable Limit Shares']

    # Market share of each broker across all brokers
    group1 = df.groupby(by=['Entry firm display'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()

    # Total share volume across all brokers
    total_shares = df['mkt_mktbl_shares'].sum()

    df1['mkt_mktbl_shares_total'] = total_shares

    df1['mkt_mktbl_share_prop'] = (df1['mkt_mktbl_shares'] / df1['mkt_mktbl_shares_total']) * 100

    df1 = df1.sort_values(by=['mkt_mktbl_share_prop'], ascending=False)

    # This is the first column in Table 2.
    df1.to_csv('../../data/tables/table2_column_1.csv', index=False)
    del group1
    del df1
    del total_shares

    # Calculate the market share across time
    group1 = df.groupby(by=['Route firm display', 'Entry firm display'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()

    group = df1.groupby(by=['Entry firm display'])

    total_shares = group.agg({
        'mkt_mktbl_shares': 'sum'
    })
    total_shares = total_shares.reset_index()
    total_shares.columns=['Entry firm display', 'mkt_mktbl_shares_total']

    df1 = df1.merge(total_shares, on=['Entry firm display'])

    df1['mkt_mktbl_share_prop'] = ((df1['mkt_mktbl_shares'] / df1['mkt_mktbl_shares_total'])) * 100

    # Do a pivot table across year month so we incert zeros for months where we have no routing to a specific wholesaler
    df_pivot2 = df1.pivot_table(index=['Entry firm display'], columns=['Route firm display'], values=['mkt_mktbl_share_prop'], fill_value=0)
    df_pivot2 = df_pivot2.reset_index()
    columns = [
            'Entry firm display',
            'Bank of America Merrill Lynch',
            'Citadel Securities, LLC',
            'G1 Execution Services, LLC',
            'Jane Street Capital, LLC',
            'Morgan Stanley & Co., LLC',
            'Two Sigma Securities, LLC',
            'UBS Securities, LLC',
            'Virtu Americas, LLC',
        ]
    df_pivot2.columns = columns

    # These are the remaining columns in Table 2.
    df_pivot2.to_csv('../../data/tables/table_2_remainder.csv', index=False)

    # We then set up and format the table in excel.

if __name__ == "__main__":
    table_2()
