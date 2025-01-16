# Replication code for “The Retail Execution Quality Landscape” by Anne Haubo Dyhrberg, Andriy Shkilko, and Ingrid Werner

## Software

The code runs using Python version 3.9.17, SAS version 19.4, and Stata version 18.5. In Stata we use the packages reghdfe and outreg2 which need to be installed by the user.

## Data

We obtain our SEC Rule 605 and 606 data from a firm that specializes in trading cost analyses. Therefore, the data provided in the Data directory is pseudo data to illustrate the data structure.

We compliment the Rule 605 and 606 data with CRSP data available Wharton Research Data Services.

Below is a list of the data files and definitions of variables within the files.

SEC Rule 605 Data: filename.csv

* symbol: the ticker symbol of the stock.
* date: the month formatted as YYYY/MM.
* entry: the wholesaler.
* type: the type of order (market or marketable limit)
* whol: a dummy variable indicating if the market center is a wholesaler (whol = 1) or an exchange (whol = 0).
* ordersize: the order size in bins 100-499, 500-999, 10

Rule 606 Data: filename.csv

*

CRSP: filename.csv

* symbol: the ticker symbol of the stock.
* date: the month formatted as YYYY/MM.
* prc: the price of the stock in USD.
* volume: the traded volume in shares.

## Code

To create the tables in the paper run the code listed below.

### Figures

To produce the figures in the paper run the code in the folder ./figures. The code specifies how to get the input data.

### Tables

To produce the tables in the paper run the code in the folder ./tables. The code specifies the input data and the formatting of the data if that is done beyond the script.
