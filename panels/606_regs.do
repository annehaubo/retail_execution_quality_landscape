* This regression greates the data graphed in Figure 3.

cd "../data/"

set more off

erase 606_reg_output.xls
erase 606_reg_output.txt

* The input dataset is created by running ./605_to_merge_w_606.sas which collapses
* 605 data to merge with 606 and 606_605_merge.py which collapses 606 data to merge with 605
* merges the data.

clear
import delimited using "../data/606_605_data.csv", clear

gen log2_vwppimpact = ln(vwppimpact)/ln(2)

* Using log2 for y_variables too 

reghdfe log2_vwppimpact broker_1 broker_2 broker_3 broker_4 broker_6 broker_7 broker_8 broker_9 broker_10, absorb(yearmonth) cluster(yearmonth)
outreg2 using 606_reg_output.xls, bdec(3) sdec(2) symbol(***,**,*) alpha(0.01,0.05,0.1) adjr2
estimates store model1
coefplot model1, drop(_cons) xtitle(Price Impact (bps)) xline(0) mlabel format(%9.0f) mlabposition(12) mlabgap(*2)
graph export 606_reg_vwppimpact.png, replace

* Test the significance of the Robinhood baseline
lincom broker_1 + broker_2 + broker_3 + broker_4 + broker_6 + broker_7 + broker_8 + broker_9 + broker_10



