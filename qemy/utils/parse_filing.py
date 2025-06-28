import pandas as pd

key_list_units = [
    'USD',
    'USD/shares',
    'shares',
]

def get_metric_df(facts, keylist, quarters=40):
    for key in keylist:
        try:
            if key in facts['facts']['us-gaap']:
                unit = None
                unit_keys = facts['facts']['us-gaap'][key]['units']
                for try_key in key_list_units:
                    if try_key in unit_keys:
                        unit = try_key
                        break
                if unit is None:
                    unit = 'USD'
                raw = facts['facts']['us-gaap'][key]['units'].get(unit, [])[-quarters:]
                data = []
                for d in raw:
                    if 'val' in d and d['val'] is not None:
                        entry = {
                            'val': d['val'],
                            'filed': pd.to_datetime(d['filed'], errors='coerce'),
                            'form': d.get('form')
                        }
                        data.append(entry)
                df = pd.DataFrame(data)
                df = df.dropna(subset=['filed'])
                df = df.sort_values('filed').drop_duplicates('filed', keep='last')
                return df.reset_index(drop=True)
        except Exception:
            continue
    return pd.DataFrame(columns=['val', 'filed', 'form'])

