import pandas as pd
from numbers import Number
from qemy.core.models.dcf import get_dcf_eval
from qemy.data.api_edgar import SEC_Filings
from qemy.data.api_edgar_bulk import bulk_refresh

#================================== EDGAR ====================================#

def dcf(arg):
    get_dcf_eval(arg)

def filing(arg, ticker_df) -> pd.DataFrame | None:
    if ' -r' in arg:
        ticker = arg.replace('-r', '').strip().upper() 
        use_requests = True
    elif ' --request' in arg:
        ticker = arg.replace('--request', '').strip().upper() 
        use_requests = True
    else:
        ticker = arg.strip().upper()
        use_requests = False
    print(f"Fetching latest 10K/10Q filing metrics for {ticker}")
    try:
        filing_df = SEC_Filings(ticker=ticker, use_requests=use_requests).get_metrics() 
        if isinstance(filing_df, pd.DataFrame): 
            ticker_df[ticker] = filing_df[ticker]
            print(filing_df.to_string(justify='left', formatters={
                ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
            }))
            if isinstance(ticker_df, pd.DataFrame):
                return ticker_df
            else:
                return None
    except:
        print("cli_edgar\nCould not fetch filing metrics, try another ticker.")

def filing_metric(arg):
    ticker = arg.strip().upper()
    try:
        metric_df = SEC_Filings(ticker=ticker).get_metric_history()
        if isinstance(metric_df, pd.DataFrame): 
            print(metric_df.to_string(justify='left', formatters={
                ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
            }))
    except:
        print("cli_edgar\nCould not fetch metric, try another ticker")

def bulk_refresh():
    confirm = input("All previous bulk data will be overwritten.\nAre you sure? (yes/no): ")
    if confirm.strip().lower() == 'yes':
        try:
            bulk_refresh()
        except Exception as e:
            print(f"cli_edgar\nBulk refresh failed. Error:\n{e}")

