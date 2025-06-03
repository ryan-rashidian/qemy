import pandas as pd
from backend.core.dcf import get_dcf_eval
from backend.fetch.api_edgar import SEC_Filings
from backend.fetch.api_edgar_bulk import bulk_refresh
#=============================================================================#
################################### SEC #######################################
#=============================================================================#
def dcf(arg):
    get_dcf_eval(arg)
#=============================================================================#
def filing(arg, ticker_df) -> pd.DataFrame | None:
    if ' -r' in arg:
        ticker = arg.replace('-r', '').strip().upper() 
        use_requests = True
    if ' --request' in arg:
        ticker = arg.replace('--request', '').strip().upper() 
        use_requests = True
    else:
        ticker = arg.strip().upper()
        use_requests = False
    print(f"Fetching latest 10K/10Q filing metrics for {ticker}")
    try:
        df = SEC_Filings(ticker=ticker, use_requests=use_requests).get_metrics() 
        if isinstance(df, pd.DataFrame): 
            ticker_df[ticker] = df[ticker]
            print(df.to_string(justify='left', formatters={
                ticker: lambda x: f"{x:,}" if isinstance(x, (int, float)) else x
            }))
            if isinstance(ticker_df, pd.DataFrame):
                return ticker_df
            else:
                return None
    except:
        print('Could not fetch filing metrics, please try another ticker.')
#=============================================================================#
def bulk_refresh():
    confirm = input("All previous bulk data will be overwritten.\nAre you sure? (yes/no): ")
    if confirm.strip().lower() == 'yes':
        try:
            bulk_refresh()
        except Exception as e:
            print(f"Bulk refresh failed. Error:\n{e}")

