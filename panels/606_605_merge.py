import pandas as pd
import numpy as np

def extract_routing():
    '''
    This function creates the dataset to run the broker toxicity regressions in 606_regs.do.
    '''

    df = pd.read_csv('../../data/606_data.csv', parse_dates=['Year Month'])

    # Set the shares to 0 if we don't have data otherwise the sum may be missing if one component is missing
    for share in ['Estimated Market Shares', 'Estimated Marketable Limit Shares']:
        df[share] = np.where(
            (df[share].isnull() == True),
            0,
            df[share]
        )

    df['mkt_mktbl_shares'] = df['Estimated Market Shares'] + df['Estimated Marketable Limit Shares']

    # Data across all stocks
    # Sum df across symbol group
    group1 = df.groupby(by=['Route firm display', 'Market center', 'Entry firm display', 'Year Month'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()

    group = df1.groupby(by=['Route firm display', 'Year Month'])

    total_shares = group.agg({
        'mkt_mktbl_shares': 'sum'
    })
    total_shares = total_shares.reset_index()
    total_shares.columns=['Route firm display', 'Year Month', 'mkt_mktbl_shares_total']

    df1 = df1.merge(total_shares, on=['Route firm display', 'Year Month'])

    df1['mkt_mktbl_share_prop'] = (df1['mkt_mktbl_shares'] / df1['mkt_mktbl_shares_total'])

    # Calculate the log2(xt/xj) where xt is a broker proportion and xj is Robinhood.
    # To do this we need to deal with the zeros as we cannot take the log of zero.
    # Use the method (2/3)_min(x)

    # Use only the non zero values
    min_prop = df1[(df1['mkt_mktbl_share_prop'] > 0)]
    min_prop = min_prop['mkt_mktbl_share_prop'].min()
    print(min_prop*(2/3))

    df_pivot = df1.pivot_table(index=['Route firm display', 'Year Month', 'Market center'], columns=['Entry firm display'], values=['mkt_mktbl_share_prop'], fill_value=np.nan)
    df_pivot = df_pivot.reset_index()
    columns = [
        'Route firm display', 
        'Year Month', 
        'Market center',
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
    df_pivot.columns = columns

    # Calculate the log ratio
    df_pivot = df_pivot.fillna(min_prop*(2/3))
    df_pivot = df_pivot.replace(to_replace=0, value=min_prop*(2/3))
    del min_prop

    for broker in columns[3:]:
        if broker == 'Robinhood Securities LLC':
            continue
        df_pivot[broker] = np.log2((df_pivot[broker] / df_pivot['Robinhood Securities LLC']))

    df_pivot.to_csv('../../data/606_data_whol_prop_routing.csv', index=False)
    del group
    del group1
    del df_pivot
    del total_shares

def merge(file1, file2, bygroups, outputfile):
    '''
    This function merges the transformed 606 and 605 data which is the input file 
    in ./606_regs.do
    '''

    df = pd.read_csv(f'../../data/{file1}.csv', parse_dates=['Year Month'])

    # This dataset is produced by running the code ./605_to_merge_w_606.sas
    df1 = pd.read_csv(f'../../data/{file2}.csv', parse_dates=['date'])

    df1['Year Month'] = pd.to_datetime(df1['date'], format='%Y%m')
    df1 = df1.drop(columns=['date'])

    if file2 == '605_whol_symbol_group_date':
        df1 = df1.rename(columns={
            'symbol_group': 'Symbol Group',
            'entry': 'Market center',
        })

    elif file2 == '605_whol_date':
        df1 = df1.rename(columns={
            'entry': 'Market center',
        })

    elif file1 == '606_data_top2_prop_routing':
        df = df.rename(columns={
        'Route firm display': 'entry_group',
    })

    df = df.merge(df1, on = bygroups, how='left')

    df.to_csv(f'../../data/{outputfile}.csv', index=False)

if __name__ == "__main__":
    extract_routing()

    merge(
        file1='606_data_whol_prop_routing',
        file2='605_whol_date',
        bygroups=['Year Month', 'Market center'],
        outputfile='606_605_data'
        )
