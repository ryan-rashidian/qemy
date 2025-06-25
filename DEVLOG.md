# Development Log

## Known Issues:

- [ ] (Non-critical) Total debt metric for filings still incomplete or outdated ~50% of time. Solutions known; Fixes are in progress.
- [ ] (Non-critical) As a result of some testing, current filings metrics have ~90% success for accuracy (with exception of total debt, referenced in previous issue). Further refinement is needed and planned. Note: most inconsistent results in financial services sector.   
- [ ] (Non-critical) P/E ratio assumes that 10k filings are reporting a cumulative eps, which is not always the case. It needs to factor in cases where: 
    - 1. Last 10k filing reported a quarterly eps, and there IS a cumulative eps reported within the previous 3 10q filings. 
    - 2. Last 10k filing reported a quarterly eps, and there IS NOT a cumulative eps reported within the previous 3 10q filings.

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

### Note (2025-06-24):

- Now that the road-map for v0.1.0 is almost completed, and most of the core design decisions have been settled, Qemy is now officially out of its prototyping stage. Changes or overhauls to the user CLI or developer facing SDK will begin to be tracked in a change-log after the v0.1.0 release.

