options ls=max ps=max nocenter nodate threads obs=max; 

data one; 
length symbol $10. entry $16.;
infile "...\605_data.csv" dlm="," dsd lrecl=1000 firstobs=2;
input symbol $ entry $ date whol sharesexecuted atorbetter priceimproved effectivespread priceimpact quotedspread realizedspread prc vol range;
if whol=1;

proc sort data=one; by symbol entry date;

proc means data=one sum noprint; var sharesexecuted; by symbol entry date; output out=tvol sum=tvol;

data one; merge one tvol; by symbol entry date; if tvol ne . and tvol ne 0;
prsp=realizedspread/prc;
vwprsp=(sharesexecuted/tvol)*prsp;

proc means data=one sum mean noprint; var sharesexecuted vwprsp prc range vol; by symbol entry date; 
	output out=one sum=shex vwprsp a1-a3 mean=b1 b2 prc range vol;

proc sort data=one; by symbol date;
proc means data=one sum noprint; var shex; by symbol date; output out=tvol sum=tvol;
data one; merge one tvol; by symbol date; if tvol ne . and tvol ne 0;

vwprsp=(shex/tvol)*vwprsp;

proc means data=one sum mean noprint; var shex vwprsp prc range vol; by symbol date; 
	output out=one sum=shex vwprsp a1-a3 mean=b1 b2 prc range vol;

data one; set one;

vwprsp=vwprsp*10000;
shex=log(shex);
range=range*100; 
if vol ne 0 then vol=log(vol);
prc=log(prc);

drop a1-a3 b1 b2;

proc sort data=one; by symbol date;

*BEG. Splits pseudo data into four groups of stocks of 147, 148, 149, and 149;
proc means data=one n noprint; var date; by symbol; output out=stocks n=a;
data stocks; set stocks; n+1;
if n le 147 then g0=0; else if g0 ne 1 then g0=0;
if n gt 147 and n le 295 then g1=1; else if g1 ne 1 then g1=0;
if n gt 295 and n le 444 then g2=1; else if g2 ne 1 then g2=0;
if n gt 444 then g3=1; else if g3 ne 1 then g3=0;
keep symbol g0-g3;
data one; merge one stocks; by symbol;
*END. Splits pseudo data into four groups of stocks of 147, 148, 149, and 149;

proc export data=one outfile='...\stata_output.dta' dbms=stata replace; run;
