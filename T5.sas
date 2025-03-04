options ls=max ps=max nocenter nodate threads; 

data combine; 
length symbol $10. entry $16.;
infile "...\605_data.csv" dlm="," dsd lrecl=1000 firstobs=2;
input symbol $ entry $ date whol sharesexecuted atorbetter priceimproved effectivespread priceimpact quotedspread realizedspread prc vol range;

if whol=1;

proc sort data=combine; by symbol entry date;
proc means data=combine sum noprint; var sharesexecuted; by symbol entry date; output out=tvol sum=tvol;

data combine; merge combine tvol; by symbol entry date; if tvol ne . and tvol ne 0;
pesp=effectivespread/prc;
ppimpact=priceimpact/prc;
prsp=realizedspread/prc;

vwpesp=(sharesexecuted/tvol)*pesp;
vwppimpact=(sharesexecuted/tvol)*ppimpact;
vwprsp=(sharesexecuted/tvol)*prsp;

proc means data=combine sum mean noprint; var sharesexecuted vwpesp vwppimpact vwprsp vol; by symbol entry date; 
	output out=combine sum=shex vwpesp vwppimpact vwprsp a1 mean=b1-b4 vol;

data combine; set combine;

if entry="market_center_1" or entry="market_center_3" then top2=1; else if top2 ne 1 then top2=0;

drop a1 b1-b4;

vwpesp=vwpesp*10000;
vwppimpact=vwppimpact*10000;
vwprsp=vwprsp*10000;

shex=log(shex);
if vol ne 0 then vol=log(vol*100);
os=shex-vol;

proc sort data=combine; by date entry;
proc means data=combine mean noprint; var os; by date entry; output out=combin mean=mos;
data combine; merge combine combin; by date entry;
dos=os-mos;
proc sort data=combine; by symbol date entry;

proc export data=combine outfile='...\stata_output.dta' dbms=stata replace; run;
