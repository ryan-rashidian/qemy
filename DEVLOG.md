# Development Log

## Known Issues:

- [ ] (Non-critical) Total debt metric for filings still incomplete or outdated ~50% of time. Solutions known; Fixes are in progress.
- [ ] (Non-critical) As a result of some testing, current filings metrics have ~90% success for accuracy (with exception of total debt, referenced in previous issue). Further refinement is needed and planned. Note: most inconsistent results in financial services sector.   

## Ideas:

- Cover all the basic metrics, ratios, etc. (e.g. Sharpe, PE, PEG, etc.)
- Stock screening and filtering.
- Separate filing commands: 'Income Statement', 'Balance Sheet', 'Cash Flow Statement' 
- IFRS filing support in SEC_Filings parser and currency conversion. 
- sklearn model that is trained on valuation data as features -> makes predictions and evaluates feature importance -> feature importance can be used to weigh different filtering/screening conditions. (Batch learning, train on demand, simple machine learning pipeline.)
- For last idea to work, metrics will need to be properly pre-processed: scaled and normalized (z-score/min-max).      

## Log

### Note (2025-06-03):

- This is my first serious project on GitHub. Earlier commits show my learning curve with git, and workflow habits. Since then, I've been refining my process. - Thanks for understanding.

