from datetime import datetime
from dateutil.relativedelta import relativedelta

def parse_period(period_str):
    now = datetime.now()
    unit = period_str[-1].upper()
    value = int(period_str[:-1])

    if unit == 'D':
        start_date = now - relativedelta(days=value)
    elif unit == 'W':
        start_date = now - relativedelta(weeks=value)
    elif unit == "M":
        start_date = now - relativedelta(months=value)
    elif unit == "Y":
        start_date = now - relativedelta(years=value)
    else:
        raise ValueError("Invalid period format. Use D, W, M, or Y")

    return start_date.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d')
