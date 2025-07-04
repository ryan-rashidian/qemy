"""Parser for companyfacts JSON files.

This module is used internally for /edgar/ parsing.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)

key_list_units = [
    'USD',
    'USD/shares',
    'shares',
]

def get_concept(
    facts: dict, 
    xbrl_tags: tuple, 
    quarters: int=10, 
    latest: bool=False
) -> pd.DataFrame | float | None:
    """Concept search and retrieval.

    Iterates through given xbrl_tags and searches for matching us-gaap key.

    Args:
        facts (dict): companyfacts from SEC EDGAR API
        xbrl_tags (tuple): Ordered strings of XBRL taxonomy tags
        quarters (int): Number of quarters to fetch
        latest (bool): True returns only latest value as float

    Returns:
        pd.DataFrame: comlumns=['val', 'filed', 'form'], quarterly rows
        float: Latest concept value (returned with 'latest = True' arg) 
        None: If incorrect inputs or parsing logic fails 
    """
    for tag in xbrl_tags:

        try:
            if tag in facts['facts']['us-gaap']:
                logger.info(f"'{tag}' found in facts")
                unit = None
                unit_keys = facts['facts']['us-gaap'][tag]['units']
                for try_key in key_list_units:
                    if try_key in unit_keys:
                        logger.info(f"'{try_key}' found in facts...['units']")
                        unit = try_key
                        break
                if unit is None:
                    logger.warning(f"facts...['units'] no match found")
                    unit = 'USD'

                raw_facts = facts['facts']['us-gaap'][tag]['units']
                logger.info(f"{len(raw_facts.get(unit, []))} filings found")
                # Slice quarters * 3 to account for duplicates
                raw_facts = raw_facts.get(unit, [])[(-quarters * 3):]
                concept_data = []
                for rf in raw_facts:
                    if 'val' in rf and rf['val'] is not None:
                        # 'filed' and 'form' meta data for each 'val'
                        filed = pd.to_datetime(rf['filed'], errors='coerce')
                        entry = {
                            'val': rf['val'],
                            'filed': filed,
                            'form': rf.get('form')
                        }
                        concept_data.append(entry)

                concept_df = pd.DataFrame(concept_data)
                concept_df = concept_df.dropna(subset=['filed'])
                concept_df = concept_df.sort_values('filed')
                concept_df = concept_df.drop_duplicates('filed', keep='last')
                concept_df = concept_df.reset_index(drop=True)
                concept_df = concept_df.tail(quarters)
                # Make sure 'val' column is float
                concept_df['val'] = concept_df['val'].astype(float)

                if latest:
                    if not concept_df.empty:
                        return float(concept_df['val'].iloc[-1])
                    else:
                        return None

                return concept_df

            else:
                logger.warning(f"'{tag}' not found in facts")
                continue

        except Exception as e:
            logger.exception(f"Exception:\n{e}")
            continue

    logger.warning(f"No matches found in facts\n{xbrl_tags}")
    return None

