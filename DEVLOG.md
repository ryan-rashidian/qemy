# Development Log

## Known Issues:

- [x] (Crash) Needs error handling when DCF model fails to find certain metrics.
- [x] (Non-critical) Parsing logic in SEC_Filings class is slightly inaccurate. Filing data is not always in chronological order. The issue has been solved in testing, and a fix will be implemented soon. 
- [x] (Non-critical) Total debt metric needs a pre-processing step to aggregate component metrics (short term, long term, current portion, etc.) when a single total debt value is not reported in the filing being parsed.
- [x] (Non-critical) DCF model is not yet factoring a company's net debt metric into the calculation. Waiting for implementation of better parsing logic, referenced in the previous issue. 
- [ ] (Non-critical) Total debt metric for filings still incomplete or outdated ~50% of time. Solutions known; Fixes are in progress.
- [ ] (Non-critical) As a result of some testing, current filings metrics have ~90% success for accuracy (with exception of total debt, referenced in previous issue). Further refinement is needed and planned. Note: most inconsistent results in financial services sector.   
- [ ] (UX) CLI commands are messy after adding several features - a full re-structure is needed and planned.  

## Ideas:

- Cover all the basic metrics, ratios, etc. (e.g. Sharpe, PE, PEG, etc.)
- Stock screening and filtering.
- Sections for filing commands: 'Income Statement', 'Balance Sheet', 'Cash Flow Statement' 
- IFRS filing support in SEC_Filings parser and currency conversion. 
- "Modes" - or organized sub-sections within the CLI for plots, models, etc. 
- Plugin architecture for qemy CLI models, plotting, etc. 
- sklearn model that is trained on valuation data as features -> makes predictions and evaluates feature importance -> feature importance can be used to weigh different filtering/screening conditions. (Batch learning, train on demand, simple machine learning pipeline.)
- For last idea to work, metrics will need to be properly pre-processed: scaled and normalized (z-score/min-max).      

## Log

### Note (2025-06-03):

- This is my first serious project on GitHub. Earlier commits show my learning curve with git, and workflow habits. Since then, I've been refining my process. - Thanks for understanding.

