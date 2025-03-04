use stata_output.dta, clear
set more off

/***BEG. Table 5.
encode symbol, gen(s)
reghdfe vwppimpact top2 [pweight=vol], noconst absorb(s#date) cluster(symbol date)
reghdfe vwprsp top2 [pweight=vol], noconst absorb(s#date) cluster(symbol date)
reghdfe vwprsp top2 mos dos [pweight=vol], noconst absorb(s#date) cluster(symbol date)
reghdfe vwpesp top2 [pweight=vol], noconst absorb(s#date) cluster(symbol date)
***END. Table 5.*/

/***BEG. Table 6, Panel A.
encode symbol, gen(s)
reghdfe depvar indvar mindvar [pweight=vol], noconst absorb(s#date entry) cluster(symbol date)
***END. Table 6, Panel A.*/

/***BEG. Table 6, Panels B-D.
*Use mindvar when computing Panels B & C.
*Use both mindvar and auxvar1 when computing Panel D.
reghdfe depvar mindvar /*auxvar1*/, noconst absorb(entry date) cluster(date)
***END. Table 6, Panels B-D.*/

/***BEG. Table 7.
reghdfe vwprsp g1 g2 g3 [pweight=vol], noconst absorb(date) cluster(symbol date)
reghdfe vwprsp g1 g2 g3 prc range [pweight=vol], noconst absorb(date) cluster(symbol date)
reghdfe vwprsp g1 g2 g3 prc range shex [pweight=vol], noconst absorb(date) cluster(symbol date)
reghdfe vwprsp g1 g2 g3 prc range vol [pweight=vol], noconst absorb(date) cluster(symbol date)
***END. Table 7.*/

/***BEG. Table 8.
encode symbol, gen(s)
*Replace vwprsp with vwpesp as needed
reghdfe vwprsp whol wholpost [pweight=vol], noconst absorb(p=s#date) cluster(symbol date)
***END. Table 8.*/

/***BEG. Figure 5.
encode symbol, gen(s)
reghdfe vwprsp whol wholpost [pweight=vol], noconst absorb(p=s#date) cluster(symbol date) resid
predict xb, xb
predict res, r
gen yhat = xb + p + res
keep if whol==1
egen mean = mean(yhat), by(date)
bysort date: ci means yhat
***END. Figure 5.*/