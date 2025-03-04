import pandas as pd

def table_2():
    '''
    This function calculates the average broker market share and 
    the average wholesaler market share for each broker. 
    These results are presented in Table 2 in the paper.
    '''

    df = pd.read_csv('../../data/606_data.csv', parse_dates=['date'])

    df['mkt_mktbl_shares'] = df['mkt_shares'] + df['mktbl_shares']

    # Market share of each broker across all brokers
    group1 = df.groupby(by=['broker'])
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
    group1 = df.groupby(by=['market_center', 'broker'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()

    group = df1.groupby(by=['broker'])

    total_shares = group.agg({
        'mkt_mktbl_shares': 'sum'
    })
    total_shares = total_shares.reset_index()
    total_shares.columns=['broker', 'mkt_mktbl_shares_total']

    df1 = df1.merge(total_shares, on=['broker'])

    df1['mkt_mktbl_share_prop'] = ((df1['mkt_mktbl_shares'] / df1['mkt_mktbl_shares_total'])) * 100

    # Do a pivot table across date so we incert zeros for months where we have no routing to a specific wholesaler
    df_pivot2 = df1.pivot_table(index=['broker'], columns=['market_center'], values=['mkt_mktbl_share_prop'], fill_value=0)
    df_pivot2 = df_pivot2.reset_index()

    # These are the remaining columns in Table 2.
    df_pivot2.to_csv('../../data/tables/table_2_remainder.csv', index=False)

    # We then set up and format the table in excel.

if __name__ == "__main__":
    table_2()
