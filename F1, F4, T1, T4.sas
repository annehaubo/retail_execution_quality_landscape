options ls=max ps=max nocenter nodate threads obs=max; 

data combine; 
length symbol $10. entry $16.;
infile "...\605_data.csv" dlm="," dsd lrecl=1000 firstobs=2;
input symbol $ entry $ date whol sharesexecuted atorbetter priceimproved effectivespread priceimpact quotedspread realizedspread prc vol range;
if whol=1;

/*BEG. Table 1. Comment out when working with Figures 1 and 4 and Table 4;
merger=1;
proc sort data=combine; by entry;
proc means data=combine sum noprint; var sharesexecuted; by entry; id merger; output out=combine (drop=_type_ _freq_) sum=shex;
proc means data=combine sum noprint; var shex; id merger; output out=combin (drop=_type_ _freq_) sum=tshex;
data combine; merge combine combin; by merger;
share=shex/tshex;
proc print data=combine; var entry share; run;
*END. Table 1. Comment out when working with Figures 1 and 4 and Table 4;*/

/*BEG. Figure 1. Comment out when working with Figure 4 and Tables 1 and 4;
proc sort data=combine; by symbol entry date;
proc means data=combine sum noprint; var sharesexecuted; by symbol entry date; output out=combine sum=shex;
proc means data=combine mean noprint; var shex; by symbol entry; output out=combine mean=shex;
proc means data=combine sum noprint; var shex; by symbol; output out=combin sum=tshex;
data combine; merge combine combin; by symbol;
sh=(100*shex/tshex)**2;
proc means data=combine sum noprint; var sh; by symbol; output out=combine (drop=_type_ _freq_) sum=hhi;
proc print data=combine noobs; run;
*END. Figure 1. Comment out when working with Figure 4 and Tables 1 and 4;*/

/*BEG. Figure 4. Comment out when working with Figure 1 and Tables 1 and 4;
proc sort data=combine; by date entry;
proc means data=combine sum noprint; var sharesexecuted; by date entry; output out=combine (drop=_type_ _freq_) sum=shex;
proc means data=combine sum noprint; var shex; by date; output out=combin (drop=_type_ _freq_) sum=tshex;
data combine; merge combine combin; by date;
if entry="market_center_10";
share=shex/tshex;
proc print data=combine; var date share; run;
*END. Table 1. Comment out when working with Figure 1 and Tables 1 and 4;*/

*BEG. Table 4 all the way down;
proc sort data=combine; by symbol date;
proc means data=combine sum mean noprint; by symbol date; var sharesexecuted vol; output out=combin sum=shex a mean=b vol;
proc means data=combin sum noprint; by symbol; var shex vol; output out=combin sum=shex vol;
data combin; set combin; share=shex/(vol*100);
proc means data=combin mean noprint; var share; output out=combin mean=share;
proc print data=combin (obs=500); run; *% of volume for Table 4;

/*BEG. Use when computing Panel B of Table 4, otherwise comment out; 
sharesexecuted=sharesexecuted*prc;
*END. Use when computing Panel B of Table 4, otherwise comment out;*/

data combine; set combine;
pqsp=quotedspread/prc;
pesp=effectivespread/prc;
ppimpact=priceimpact/prc;
prsp=realizedspread/prc;

proc means data=combine sum noprint; var sharesexecuted; by symbol; output out=tvol sum=tvol;
data combine; merge combine tvol; by symbol; if tvol ne . and tvol ne 0;

vwpqsp=(sharesexecuted/tvol)*pqsp;
vwpesp=(sharesexecuted/tvol)*pesp;
vwppimpact=(sharesexecuted/tvol)*ppimpact;
vwprsp=(sharesexecuted/tvol)*prsp;
vwpimproved=(sharesexecuted/tvol)*priceimproved;
vwatbet=(sharesexecuted/tvol)*atorbetter;

merger=1;

proc means data=combine sum noprint; var sharesexecuted vwpqsp vwpesp vwppimpact vwprsp vwpimproved vwatbet; by symbol; id merger;
	output out=combine sum=shex vwpqsp vwpesp vwppimpact vwprsp vwpimproved vwatbet;

*BEG. For Panel A of Table 4. Comment out when computing Panel B of Table 4;
proc means data=combine mean noprint; var vwpqsp vwpesp vwppimpact vwprsp vwpimproved vwatbet;
	output out=combine mean=vwpqsp vwpesp vwppimpact vwprsp vwpimproved vwatbet;
*END. For Panel A of Table 4. Comment out when computing Panel B of Table 4;

/*BEG. For Panel B of Table 4. Comment out when computing Panel A of Table 4;
proc means data=combine sum noprint; var shex; id merger; output out=tvol sum=tvol;
data combine; merge combine tvol; by merger; if tvol ne . and tvol ne 0;

vwpqsp=(shex/tvol)*vwpqsp;
vwpesp=(shex/tvol)*vwpesp;
vwppimpact=(shex/tvol)*vwppimpact;
vwprsp=(shex/tvol)*vwprsp;
vwpimproved=(shex/tvol)*vwpimproved;
vwatbet=(shex/tvol)*vwatbet;

proc means data=combine sum noprint; var vwpqsp vwpesp vwppimpact vwprsp vwpimproved vwatbet;
	output out=combine sum=vwpqsp vwpesp vwppimpact vwprsp vwpimproved vwatbet;
*END. For Panel B of Table 4. Comment out when computing Panel A of Table 4;*/

data combine; set combine;

vwpqsp=vwpqsp*10000;
vwpesp=vwpesp*10000;
vwppimpact=vwppimpact*10000;
vwprsp=vwprsp*10000;

proc print data=combine noobs; var vwpimproved vwatbet vwpqsp vwpesp vwppimpact vwprsp; run; *Results for either Panel A or B of Table 4;
