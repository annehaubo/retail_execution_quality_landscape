options ls=max ps=max nocenter nodate threads obs=max; 

data one; 
length symbol $10. entry $16.;
infile "...\605_data.csv" dlm="," dsd lrecl=1000 firstobs=2;
input symbol $ entry $ date whol sharesexecuted atorbetter priceimproved effectivespread priceimpact quotedspread realizedspread prc vol range;

*BEG. For Panel A, comment out;
/*Panel B;
if entry ne "market_center_10";
*Panel C;
if entry = "market_center_10";*/
*END. For Panel A, comment out;

pesp=effectivespread/prc;
prsp=realizedspread/prc;

proc sort data=one; by whol symbol date;
proc means data=one sum noprint; var sharesexecuted; by whol symbol date; output out=tvol sum=tvol;
data one; merge one tvol; by whol symbol date; if tvol ne . and tvol ne 0;

vwpesp=(sharesexecuted/tvol)*pesp;
vwprsp=(sharesexecuted/tvol)*prsp;

proc means data=one sum mean noprint; var vwpesp vwprsp vol; by whol symbol date; 
	output out=one sum=vwpesp vwprsp a1 mean=b1 b2 vol;

data one; set one;

vwpesp=vwpesp*10000;
vwprsp=vwprsp*10000;

if vol ne 0 then vol=log(vol);

drop a1 b1 b2 _type_ _freq_;

if date ge 202104 and date le 202106 then post=0; else if date ge 202110 and date le 202112 then post=1; if post ne .;

wholpost=whol*post;
keep whol symbol date vwpesp vwprsp post wholpost vol;

proc export data=one outfile='...\stata_output.dta' dbms=stata replace; run;
