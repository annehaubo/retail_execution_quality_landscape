import pandas as pd
import numpy as np

def changes_in_routing():
    '''
    This function calculates the average absolute change 
    in routing for each broker wholesaler across months.
    It also calculates the high low routing changes.
    These results are presented in Table 3 in the paper and Table A1 in the Internet Appendix.
    '''

    df = pd.read_csv('../../data/606_data.csv', parse_dates=['date'])

    df['mkt_mktbl_shares'] = df['mkt_shares'] + df['mktbl_shares']

    # Market share of each broker across all brokers
    group1 = df.groupby(by=['broker', 'date'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()

    # Sum across S&P500 and Other stocks
    group1 = df.groupby(by=['market_center', 'broker', 'date'])
    df1 = group1.agg({
        'mkt_mktbl_shares': 'sum'
    })
    df1 = df1.reset_index()
    del group1

    # Calculate the market share
    group = df1.groupby(by=['broker', 'date'])

    total_shares = group.agg({
        'mkt_mktbl_shares': 'sum'
    })
    total_shares = total_shares.reset_index()
    total_shares.columns=['broker', 'date', 'mkt_mktbl_shares_total']
    del group

    df1 = df1.merge(total_shares, on=['broker', 'date'])

    df1['mkt_mktbl_share_prop'] = ((df1['mkt_mktbl_shares'] / df1['mkt_mktbl_shares_total'])) * 100

    # Do a pivot table across date so we incert zeros for months where we have no routing to a specific wholesaler
    df_pivot1 = df1.pivot_table(index=['broker', 'date'], columns=['market_center'], values=['mkt_mktbl_share_prop'], fill_value=0)
    df_pivot1 = df_pivot1.reset_index()

    wholesalers = [
        'wholesaler_1',
        'wholesaler_2',
        'wholesaler_3',
        'wholesaler_4',
        'wholesaler_5',
        'wholesaler_6',
        'wholesaler_7',
        'wholesaler_8',
    ]

    # # Calculate the change
    for wholesaler in wholesalers:

        df_pivot1[f'{wholesaler} lag'] = np.where(
            (df_pivot1['broker'] == df_pivot1['broker'].shift(1)),
            df_pivot1[wholesaler].shift(1),
            np.nan
        )

        df_pivot1[f'{wholesaler} abs_change'] = (df_pivot1[wholesaler] - df_pivot1[f'{wholesaler} lag']).abs()

        # Calcualte the start and finish market shares
        df_pivot1[f'{wholesaler}_start'] = np.where(
            (df_pivot1['date'] == '2020-01-01'),
            df_pivot1[wholesaler],
            np.nan
        )
        df_pivot1[f'{wholesaler}_start'] = np.where(
                ((df_pivot1['broker'] == 'broker_3') & (df_pivot1['date'] == '2021-07-01')),
                df_pivot1[wholesaler],
                df_pivot1[f'{wholesaler}_start']
            )

        df_pivot1[f'{wholesaler}_end'] = np.where(
            (df_pivot1['date'] == '2022-12-01'),
            df_pivot1[wholesaler],
            np.nan
        )

    # Calculate the average change by broker and wholesaler across months
    group = df_pivot1.groupby(by=['broker'])
    stats = group.agg({
        'wholesaler_1 abs_change': 'mean',
        'wholesaler_1_start': 'mean',
        'wholesaler_1_end': 'mean',
        'wholesaler_2 abs_change': 'mean',
        'wholesaler_2_start': 'mean',
        'wholesaler_2_end': 'mean',
        'wholesaler_3 abs_change': 'mean',
        'wholesaler_3_start': 'mean',
        'wholesaler_3_end': 'mean',
        'wholesaler_4 abs_change': 'mean',
        'wholesaler_4_start': 'mean',
        'wholesaler_4_end': 'mean',
        'wholesaler_5 abs_change': 'mean',
        'wholesaler_5_start': 'mean',
        'wholesaler_5_end': 'mean',
        'wholesaler_6 abs_change': 'mean',
        'wholesaler_6_start': 'mean',
        'wholesaler_6_end': 'mean',
        'wholesaler_7 abs_change': 'mean',
        'wholesaler_7_start': 'mean',
        'wholesaler_7_end': 'mean',
        'wholesaler_8 abs_change': 'mean',
        'wholesaler_8_start': 'mean',
        'wholesaler_8_end': 'mean',
    })
    stats = stats.reset_index()

    for wholesaler in wholesalers:
        stats[f'{wholesaler} start finish'] = "'" +   stats[f'{wholesaler}_start'].round().astype(int).astype(str) + '-' + stats[f'{wholesaler}_end'].round().astype(int).astype(str)

    stats = stats.drop(columns=[
        'wholesaler_1_start',
        'wholesaler_1_end',
        'wholesaler_2_start',
        'wholesaler_2_end',
        'wholesaler_3_start',
        'wholesaler_3_end',
        'wholesaler_4_start',
        'wholesaler_4_end',
        'wholesaler_5_start',
        'wholesaler_5_end',
        'wholesaler_6_start',
        'wholesaler_6_end',
        'wholesaler_7_start',
        'wholesaler_7_end',
        'wholesaler_8_start',
        'wholesaler_8_end',
    ])

    # Calculate the high lows
    stats2 = group.agg({
        'wholesaler_1': ['min', 'max'],
        'wholesaler_2': ['min', 'max'],
        'wholesaler_3': ['min', 'max'],
        'wholesaler_4': ['min', 'max'],
        'wholesaler_5': ['min', 'max'],
        'wholesaler_6': ['min', 'max'],
        'wholesaler_7': ['min', 'max'],
        'wholesaler_8': ['min', 'max'],  
    })
    stats2 = stats2.reset_index()

    columns = [
        'broker',
        'wholesaler_1 Min',
        'wholesaler_1 Max',
        'wholesaler_2 Min',
        'wholesaler_2 Max',
        'wholesaler_3 Min',
        'wholesaler_3 Max',
        'wholesaler_4 Min',
        'wholesaler_4 Max',
        'wholesaler_5 Min',
        'wholesaler_5 Max',
        'wholesaler_6 Min',
        'wholesaler_6 Max',
        'wholesaler_7 Min',
        'wholesaler_7 Max',
        'wholesaler_8 Min',
        'wholesaler_8 Max',
        
    ]
    stats2.columns = columns

    # Create a high low variable
    for wholesaler in wholesalers:
        stats2[f'{wholesaler} Low High'] = "'" +   stats2[f'{wholesaler} Min'].round().astype(int).astype(str) + '-' + stats2[f'{wholesaler} Max'].round().astype(int).astype(str)

    stats2 = stats2.drop(columns=columns[1:])

    stats = pd.concat([stats, stats2])

    stats.to_csv('../../data/table_3.csv', index=False)

    # We then format Table 3 in the paper using the absolute change.
    # Table A1 in the appendix expands on Table 3 by reporting the
    # smallest to largest and beginning to end routing statistics
    # alongside the absolute change. This formatting is done in excel.

if __name__ == "__main__":
    changes_in_routing()