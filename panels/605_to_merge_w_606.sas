/* This script calculates the */

* Import 605 data;

* Combine data;
data combine; set import;

* Only keep the wholsalers;
if whol = 1;

if sp500 = . then sp500 = 0;
if sp500 = 1 then symbol_group = "SP500";
if sp500 = 0 then symbol_group = "Other";

ppimpact=priceimpact_tr/prc;

run; 

* We want a dataset of entry, symbol_group, date;
* First we aggregate across type (MKT and MKTBL);
proc sort data=combine; by symbol_group symbol entry date;
proc means data=combine sum noprint; var shex; by symbol_group symbol entry date; output out=tvol sum=tvol;

data combine; merge combine tvol; 
by symbol_group symbol entry date; 
if tvol ne . and tvol ne 0;

vwppimpact=(shex/tvol)*vwppimpact;

run; 

proc means data=combine sum mean noprint; 
by symbol_group symbol entry date; 
	output out=combine 

sum(shex) = shex
sum(vwppimpact) = vwppimpact;

run; 

* Then we equal weight across symbols in the symbol_group;
data combine; set combine;

vwppimpact=vwppimpact*10000;

run; 

* Average across symbol groups;
proc sort data=combine; by entry date;

proc means data=combine mean noprint; 
by entry date;
	output out=combine2 (drop = _TYPE_)
mean(vwppimpact) = vwppimpact;

run;

PROC EXPORT DATA=combine
    OUTFILE='file_path\data\605_whol_date.csv'
    DBMS=CSV REPLACE;
RUN;
