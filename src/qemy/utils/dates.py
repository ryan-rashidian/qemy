"""Date and time utility for Qemy."""

from datetime import datetime

from dateutil.relativedelta import relativedelta

from qemy.exceptions import InvalidSyntaxError


def parse_period(period_str) -> tuple[str, str]:
    """Convert shorthand period into formatted date-time strings.

    Args:
        period_str (str): shorthand period string (e.g., "2W", "4M")

    Returns:
        tuple[str, str]: tuple of start and end date strings

    Raises:
        InvalidSyntaxError: if period string syntax is invalid
    """
    period_str = period_str.strip()

    try:
        now = datetime.now()
        unit = period_str[-1].upper()
        value = int(period_str[:-1])

        match unit:
            case 'D':
                start_date = now - relativedelta(days=value)
            case 'W':
                start_date = now - relativedelta(weeks=value)
            case 'M':
                start_date = now - relativedelta(months=value)
            case 'Y':
                start_date = now - relativedelta(years=value)
            case _:
                raise InvalidSyntaxError("Invalid unit")

        return start_date.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d')

    except ValueError as e:
        raise InvalidSyntaxError(
            "Invalid period format.\n"
            "Use: D, W, M, or Y\n"
            "Usage: <INTEGER><UNITS>\n"
            "Examples: '6M', '2Y', '5D'"
        ) from e

