options ls=max ps=max nocenter nodate threads obs=max; 

data combine; 
length symbol $10. entry $16.;
infile "...\605_data.csv" dlm="," dsd lrecl=1000 firstobs=2;
input symbol $ entry $ date whol sharesexecuted atorbetter priceimproved effectivespread priceimpact quotedspread realizedspread prc vol range;
if whol=1;

proc sort data=combine; by entry symbol date;
proc means data=combine sum noprint; var sharesexecuted; by entry symbol date; output out=tvol sum=tvol;

data combine; merge combine tvol; by entry symbol date; if tvol ne . and tvol ne 0;
pesp=effectivespread/prc;
ppimpact=priceimpact/prc;
prsp=realizedspread/prc;

vwpesp=(sharesexecuted/tvol)*pesp;
vwppimpact=(sharesexecuted/tvol)*ppimpact;
vwprsp=(sharesexecuted/tvol)*prsp;

proc means data=combine sum mean noprint; var sharesexecuted vwpesp vwppimpact vwprsp vol; by entry symbol date; 
	output out=combine sum=shex vwpesp vwppimpact vwprsp a1 mean=b1-b4 vol;

proc sort data=combine; by symbol date;
proc means data=combine sum noprint; var shex; by symbol date; output out=tvol (drop=_type_ _freq_) sum=tvol;

data combine; merge combine tvol; by symbol date;

proc sort data=combine; by entry symbol date;
data combine; set combine;

*Replace realized spreads with effective spreads for Panel C; 
*vwprsp=vwpesp;
*Replace realized spreads with price impacts for the first (storage) run for Panel D. Once the storage run is complete, run as normal for the realized spreads;
*vwprsp=vwppimpact;

lentry=lag(entry); lsymbol=lag(symbol); if entry=lentry and symbol=lsymbol then lvwprsp=lag(vwprsp)*10000;
l2entry=lag2(entry); l2symbol=lag2(symbol); if entry=l2entry and symbol=l2symbol then l2vwprsp=lag2(vwprsp)*10000;
l3entry=lag3(entry); l3symbol=lag3(symbol); if entry=l3entry and symbol=l3symbol then l3vwprsp=lag3(vwprsp)*10000;

*Three lags. Comment out for one lag; 
lvwprsp=(lvwprsp+l2vwprsp+l3vwprsp)/3;

share=shex/tvol; drop a1 b1-b4;

if vol ne 0 then vol=log(vol);

keep entry symbol date share lvwprsp vol; 

*BEG. Panel A, Table 6. Comment out the next block titled Panels B-D, Table 6 before running this block;;
data combin; set combine;
if share ne 0 then logshare=log(share);

proc sort data=combin; by symbol date;
proc means data=combin mean noprint; var logshare lvwprsp; by symbol date; output out=combi (drop=_TYPE_ _FREQ_) mean=mlogshare mlvwprsp;

proc means data=combin (where=(entry ne "market_center_1")) mean noprint; var lvwprsp; by symbol date; output out=combi1 (drop=_TYPE_ _FREQ_) mean=mlvwprsp1;
proc means data=combin (where=(entry ne "market_center_3")) mean noprint; var lvwprsp; by symbol date; output out=combi2 (drop=_TYPE_ _FREQ_) mean=mlvwprsp2;
proc means data=combin (where=(entry ne "market_center_4")) mean noprint; var lvwprsp; by symbol date; output out=combi3 (drop=_TYPE_ _FREQ_) mean=mlvwprsp3;
proc means data=combin (where=(entry ne "market_center_5")) mean noprint; var lvwprsp; by symbol date; output out=combi4 (drop=_TYPE_ _FREQ_) mean=mlvwprsp4;
proc means data=combin (where=(entry ne "market_center_7")) mean noprint; var lvwprsp; by symbol date; output out=combi5 (drop=_TYPE_ _FREQ_) mean=mlvwprsp5;
proc means data=combin (where=(entry ne "market_center_10")) mean noprint; var lvwprsp; by symbol date; output out=combi6 (drop=_TYPE_ _FREQ_) mean=mlvwprsp6;

data combi; set combi;
gmlogshare=exp(mlogshare);
data combin; merge combin combi combi1-combi6; by symbol date;
proc sort data=combin; by entry symbol date;
data combin; set combin;
depvar=log(share/gmlogshare);

if entry="market_center_1" then indvar=lvwprsp-mlvwprsp1;
if entry="market_center_3" then indvar=lvwprsp-mlvwprsp2;
if entry="market_center_4" then indvar=lvwprsp-mlvwprsp3;
if entry="market_center_5" then indvar=lvwprsp-mlvwprsp4;
if entry="market_center_7" then indvar=lvwprsp-mlvwprsp5;
if entry="market_center_10" then indvar=lvwprsp-mlvwprsp6;

if entry ne "market_center_2" and entry ne "market_center_9";

proc sort data=combin; by entry date;
proc means data=combin mean noprint; var indvar; by entry date; output out=combi (drop=_type_ _freq_) mean=mindvar;

data combin; merge combin combi; by entry date;
proc sort data=combin; by entry symbol date;

proc export data=combin outfile='...\stata_output.dta' dbms=stata replace; run;
*END. Panel A, Table 6;


*BEG. Panels B-D, Table 6. Comment out the previous block titled Panel A, Table 6 before running this block;
proc sort data=combine; by entry date;
proc means data=combine mean noprint; var share lvwprsp; by entry date; output out=combin mean=share lvwprsp;

data combin; set combin;
if share ne 0 then logshare=log(share);

proc sort data=combin; by date;
proc means data=combin mean noprint; var logshare lvwprsp; by date; output out=combi (drop=_TYPE_ _FREQ_) mean=mlogshare mlvwprsp;

proc means data=combin (where=(entry ne "market_center_1")) mean noprint; var lvwprsp; by date; output out=combi1 (drop=_TYPE_ _FREQ_) mean=mlvwprsp1;
proc means data=combin (where=(entry ne "market_center_3")) mean noprint; var lvwprsp; by date; output out=combi2 (drop=_TYPE_ _FREQ_) mean=mlvwprsp2;
proc means data=combin (where=(entry ne "market_center_4")) mean noprint; var lvwprsp; by date; output out=combi3 (drop=_TYPE_ _FREQ_) mean=mlvwprsp3;
proc means data=combin (where=(entry ne "market_center_5")) mean noprint; var lvwprsp; by date; output out=combi4 (drop=_TYPE_ _FREQ_) mean=mlvwprsp4;
proc means data=combin (where=(entry ne "market_center_7")) mean noprint; var lvwprsp; by date; output out=combi5 (drop=_TYPE_ _FREQ_) mean=mlvwprsp5;
proc means data=combin (where=(entry ne "market_center_10")) mean noprint; var lvwprsp; by date; output out=combi6 (drop=_TYPE_ _FREQ_) mean=mlvwprsp6;

data combi; set combi;
gmlogshare=exp(mlogshare);
data combin; merge combin combi combi1-combi6; by date;
proc sort data=combin; by entry date;
data combin; set combin;
depvar=log(share/gmlogshare);

data combin; set combin;

data combin; set combin;
if entry="market_center_1" then indvar=lvwprsp-mlvwprsp1;
if entry="market_center_3" then indvar=lvwprsp-mlvwprsp2;
if entry="market_center_4" then indvar=lvwprsp-mlvwprsp3;
if entry="market_center_5" then indvar=lvwprsp-mlvwprsp4;
if entry="market_center_7" then indvar=lvwprsp-mlvwprsp5;
if entry="market_center_10" then indvar=lvwprsp-mlvwprsp6;

if entry ne "market_center_2" and entry ne "market_center_9";

proc sort data=combin; by entry date;
proc means data=combin mean noprint; var indvar; by entry date; output out=combi (drop=_type_ _freq_) mean=mindvar;

*For Panel D, run the code first to store the price impact variable in store1. Comment out store1 storage (next line). 
Then run again to get the realized spread. The main file and store1 will merge below for the regression that uses both realized spreads and price impacts;
/*data store1; set combi; auxvar1=mindvar; drop mindvar; run;*/

*For Panel D, uncomment store1;
data combin; merge combin combi /*store1*/; by entry date;
proc sort data=combin; by entry date;

proc export data=combin outfile='...\stata_output.dta' dbms=stata replace; run;
*END. Panels B-D, Table 6;
