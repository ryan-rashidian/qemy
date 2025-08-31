"""SEC filing concept parser."""

import logging
from dataclasses import dataclass

import pandas as pd

from qemy.exceptions import ParseError

logger = logging.getLogger(__name__)

@dataclass
class SECFiles:
    company: str
    label: str
    units: str
    description: str
    data: pd.DataFrame

def get_concept(
    facts: dict,
    xbrl_tags: tuple,
    quarters: int = 10
) -> SECFiles:
    """Concept search and retrieval.

    Parses companyfacts JSON given a tuple of possible xbrl concept names.
    Iterates through given xbrl_tags and searches for matching concept string.

    Args:
        facts (dict): companyfacts from SEC EDGAR API
        xbrl_tags (tuple): ordered strings of XBRL taxonomy concept names
        quarters (int): number of quarters to fetch

    Returns:
        ConceptFiles: dataclass containing parsed and organized concept data

    Raises:
        ParseError: if parsing fails (see logs for details)
    """
    company_name = facts.get('entityName', '')

    for tag in xbrl_tags:
        if tag not in facts['facts']['us-gaap']:
            logger.debug(f"'{tag}' not found in facts")
            continue

        logger.debug(f"'{tag}' found in facts (us-gaap)")
        concept: dict = facts['facts']['us-gaap'][tag]
        description = concept.get('description', '')
        label = concept.get('label', '')

        units_dict = concept.get('units')
        if not units_dict:
            logger.warning(f'No units found for {tag}')
            continue

        unit = next(iter(units_dict))
        concept_files_all: list = units_dict[unit]
        logger.debug(f"{len(concept_files_all)} filings found")

        try:
            # Slice quarters * 3 to buffer for duplicate removal
            concept_sliced = concept_files_all[(-quarters * 3):]
            concept_parsed = [
                {
                    'filed': pd.to_datetime(f.get('filed'), errors='coerce'),
                    'form': f.get('form'),
                    'fy': f.get('fy'),
                    'fp': f.get('fp'),
                    'end': pd.to_datetime(f.get('end'), errors='coerce'),
                    'val': f.get('val')
                }
                for f in concept_sliced
            ]
        except Exception as e:
            logger.warning(f"Parsing error: {tag}\n{e}")
            continue

        concept_df = pd.DataFrame(concept_parsed)
        concept_df.dropna(subset=['filed'], inplace=True)
        concept_df.sort_values('filed', inplace=True)
        concept_df.drop_duplicates('filed', keep='last', inplace=True)
        concept_df.reset_index(drop=True, inplace=True)
        concept_df['val'] = concept_df['val'].astype(float)
        concept_df = concept_df.tail(quarters)

        return SECFiles(
            company=company_name,
            label=label,
            units=unit,
            description=description,
            data=concept_df
        )

    logger.error(f"Concept not found. No matches in:\n{xbrl_tags}")
    raise ParseError("No matches found in facts")

