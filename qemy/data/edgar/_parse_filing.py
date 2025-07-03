"""Parser for companyfacts JSON files.

This module is used internally for /edgar/ parsing.
"""

import pandas as pd

key_list_units = [
    'USD',
    'USD/shares',
    'shares',
]

def get_concept(
    facts: dict, 
    xbrl_tags: tuple, 
    quarters: int=20, 
    latest: bool=False
) -> pd.DataFrame | float | None:
    """Concept search and retrieval.

    Iterates through given xbrl_tags and searches for matching us-gaap key.

    Args:
        facts (dict): JSON file from companyfacts
        xbrl_tags (tuple): Ordered strings of XBRL taxonomy tags
        quarters (int): Number of quarters to fetch
        latest (bool): True returns only latest value (default = False)

    Returns:
        pd.DataFrame: Quarterly rows for given concept
        float: Latest concept value (returned with 'latest = True' arg) 
        None: If incorrect inputs or parsing logic fails 
    """
    for tag in xbrl_tags:
        try:

            if tag in facts['facts']['us-gaap']:
                unit = None
                unit_keys = facts['facts']['us-gaap'][tag]['units']
                for try_key in key_list_units:
                    if try_key in unit_keys:
                        unit = try_key
                        break
                if unit is None:
                    unit = 'USD'

                raw = facts['facts']['us-gaap'][tag]['units']
                #if unit not in raw:
                #    print(f"{unit} not found in {tag}")
                #    continue
                #raw = raw[unit]
                #if not isinstance(raw, list):
                #    print(f"{tag} unit {unit} got type{raw}")
                #    continue
                #print("test1.7")
                #raw = raw[-quarters:]
                raw = raw.get(unit, [])[-quarters:]
                data = []
                for d in raw: # Sometimes, you just have to.
                    if 'val' in d and d['val'] is not None:
                        filed = pd.to_datetime(d['filed'], errors='coerce')
                        entry = {
                            'val': d['val'],
                            'filed': filed,
                            'form': d.get('form')
                        }
                        data.append(entry)

                df = pd.DataFrame(data)
                df = df.dropna(subset=['filed'])
                df = df.sort_values('filed')
                df = df.drop_duplicates('filed', keep='last')
                df = df.reset_index(drop=True)

                if latest:
                    if not df.empty:
                        return float(df['val'].iloc[-1])
                    else:
                        return None

                return df

        except Exception:
            continue

    return None

