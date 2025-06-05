import pandas as pd

def get_metric_df(facts, keylist, unit='USD', quarters=40):
    for key in keylist:
        try:
            if key in facts['facts']['us-gaap']:
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
                df = df.sort_values('filed').drop_duplicates('filed', keep='first')
                return df.reset_index(drop=True)
        except Exception:
            continue
    return pd.DataFrame(columns=['val', 'filed', 'form'])

