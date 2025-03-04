# Replication code for “The Retail Execution Quality Landscape” by Anne Haubo Dyhrberg, Andriy Shkilko, and Ingrid Werner

## Software

The code runs using Python version 3.9.17, SAS version 19.4, and Stata version 18.5. In Stata we use the packages reghdfe and outreg2 which need to be installed by the user.

## Data

We obtain our SEC Rule 605 and 606 data from a firm that specializes in trading cost analyses. Therefore, the data provided in the Data directory is pseudo data to illustrate the data structure. As a result the outputs do not match what is presented in the paper

We compliment the Rule 605 and 606 data with CRSP data available Wharton Research Data Services.

Below is a list of the data files and definitions of variables within the files.

SEC Rule 605 Data: 605_data.csv

* symbol: the ticker symbol of the stock
* date: the month formatted as YYYYMM
* market_center: the market center
* prc: the price of the stock in USD from CRSP
* vol: the traded volume in shares from CRSP
* range: the range of prices from CRSP
* whol: a dummy variable indicating if the market center is a wholesaler (whol = 1) or an exchange (whol = 0)
* sharesexecuted: executed shares and away executed shares
* atorbetter: number of shares executed at the best quotes or better
* priceimproved: number of shares that received a price improvement
* effectivespread: the effective spread in dollars
* priceimpact: the price impact in dollars
* quotedspread: the quoted spread in dollars
* realisedspread: the realized spread in dollars

Rule 606 Data: 606_data.csv

* date: the month formatted as YYYY-MM-DD. The date is always the first of the month.
* symbol_group: the symbol group which is either 'Other Stocks' or 'S&P 500'
* broker: broker identifyer
* market_center: market center identifyer
* pfof_mkt: total payments paied for market orders
* pfof_100s_mkt: payments per 100 shares for market orders
* mkt_shares: estimated market order shares
* pfof_mktbl: total payment for marketable limit orders
* pfof_100s_mktbl: payments per 100 shares for marketable limit orders
* mktbl_shares: estimated marketable limit shares

## Code

To create the figures and tables in the paper run the code in the folder. Figures are labelled F1-F5 and tables T1-T8. Most of the tables and figurs are run directly on the 606 and 605 data. Others require the user to run statistics first. These are listed in the folder ./panels/. Each code will state what to run to obtain the input data for the given table or figure.
