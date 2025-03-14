# Replication code for “The Retail Execution Quality Landscape” by Anne Haubo Dyhrberg, Andriy Shkilko, and Ingrid Werner

## Overview

The code in this replication package constructs the 8 tables and 5 figures in the paper “The Retail Execution Quality Landscape” by Anne Haubo Dyhrberg, Andriy Shkilko, and Ingrid Werner. The code runs using Python, SAS, and Stata. The replicator should expect the code to run for 1 hour depending on the replicator's hardware.

## Data Availability and Proenance Statements

We obtain our SEC Rule 605 and 606 data from a firm that specializes in trading cost analyses. Therefore, the data provided in the Data directory is pseudo data to illustrate the data structure. As a result the outputs do not match what is presented in the paper. A replicator can download the raw Rule 605 and 606 data from wholesalers and brokers directly and create the variables described in Internet Appendix sections A.3 and A.4.

We compliment the Rule 605 and 606 data with CRSP data available Wharton Research Data Services. We use the variables vol, prc, askhi, and bidlo.

### Details on each Data Source

| Data.Name    | Data.Files     | Location | Pseudo Provided |
| :----------- | :------------- | :------- | :-------------- |
| 605 data     | 605_data.csv   | data/    | TRUE            |
| 606 data     | 606_data.csv   | data/    | TRUE            |
| crsp         |                |          | FALSE           |
|              |                |          |                 |

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

## Statement about Rights

We certify that the author(s) of the manuscript have legitimate access to and permission to use the data used in this manuscript.

## Computational Requirements

The code was run on a Windows PC with an Intel(R) Xeon(R) Gold 6128 CPU @ 3.40GHz 3.39 GHz, 128 GB RAM, and 200 GB dish space as well as a MacBook Pro with an Apple M1 Pro chip, 32GB RAM, and 200GB disk space. The replicator should expect the code to run for no more than 1 hour using these hardware specification.

### Software Requirements

To run the code the replicator needs the following programs and packages:

* Stata version 19.4
    * reghdfe
    * outreg2

* SAS version 19.4

* Python version 3.9.17
    * pandas
    * numpy
    * matplotlib
    * seaborn
    * datetime

## Description of Programs/Code

To create the figures and tables in the paper run the code in the folder. Figures are labelled F1-F5 and tables T1-T8. Most of the tables and figurs are run directly on the 606 and 605 data. Others require the replicator to run statistics first. These are listed in the folder ./panels/. Each code will state what to run to obtain the input data for the given table or figure.

## Instructionf to Replicators

To replicate the results in the paper the replicator first needs to collect the public 605 and 606 data for the wholesalers and brokers as well as monthly data from the CRSP database by Wharton Research Data Services. The replicator then runs to provided code to produce all tables and figures in the paper following the overview below.

| Figure/Table # | Program            | Line Number | Output File           |
| :------------- | :----------------- | :---------- | :-------------------- |
| Figure 1       | F1.py              |             | figure_1.png          |
| Figure 2       | F2.py              |             | sankey_data.csv       |
| Figure 3       | F3.py              |             | figure_3.png          |
| Figure 4       | F4.py              |             | figure_4.png          |
| Figure 5       | F5.py              |             | figure_5.png          |
| Table 1        | F1, F4, T1, T4.sas | 9-17        | SAS Output            |
| Table 2        | T2.py              |             | table2_column_1.csv   |
|                |                    |             | table_2_remainder.csv |
| Table 3        | T3.py              |             | table_3.csv           |
| Table 4        | F1, F4, T1, T4.sas | 40-100      | SAS Output            |
| Table 5        | T5.sas             |             | SAS Output            |
| Table 6        | T6.sas             |             | SAS Output            |
| Table 7        | T7.sas             |             | SAS Output            |
| Table 8        | T8.sas             |             | SAS Output            |
|                |                    |             |                       |
