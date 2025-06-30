import pandas as pd
from qemy import _config as cfg
from qemy.utils.utils_fetch import parse_period, safe_status_get

class FREDClient:
    def __init__(self):
        self.API_KEY = cfg.FRED_API_KEY
        self.url = cfg.FRED_URL

    def _fetch_series(
            self, series_id, period='1Y', 
            frequency='m', units='pc1', 
            aggregation='avg', limit=None
    ):

        start_date, end_date = parse_period(period)
        params = {
            'series_id': series_id,
            'api_key': self.API_KEY,
            'file_type': 'json',
            'sort_order': 'desc',
            'observation_start': start_date,
            'observation_end': end_date,
            'frequency': frequency,
            'units': units,
            'aggreation_model': aggregation,
        }
        if limit:
            params['limit'] = limit

        try:
            fred_data = safe_status_get(url=self.url, params=params)
            if fred_data and fred_data.get('observations'):
                obs_df = pd.DataFrame(fred_data['observations'])
                obs_df['date'] = pd.to_datetime(obs_df['date'])
                obs_df.set_index('date', inplace=True)
                obs_df['value'] = pd.to_numeric(obs_df['value'], errors='coerce')
                return obs_df.drop(
                    columns=['realtime_start', 'realtime_end'], 
                    errors='ignore'
                )

        except Exception as e:
            print(f"data/api_fred.py Error:\n{e}")
        return None

    def get_tbill_yield(self):
        return self._fetch_series('GS1', period='1M', frequency='m', units='lin', limit=1)

    def get_cpi(self, period='1Y', units='pc1'):
        return self._fetch_series('CPIAUCSL', period, frequency='m', units=units)

    def get_gdp(self, period='1Y', units='pc1'):
        return self._fetch_series('GDP', period, frequency='q', units=units)

    def get_sentiment(self, period='1Y', units='pch'):
        return self._fetch_series('UMCSENT', period, frequency='m', units=units)

    def get_nf_payrolls(self, period='1Y', units='pc1'):
        return self._fetch_series('PAYEMS', period, frequency='m', units=units)

    def get_interest_rate(self, period='1Y', units='pc1'):
        return self._fetch_series('DFF', period, frequency='d', units=units)

    def get_jobless_claims(self, period='1Y', units='pc1'):
        return self._fetch_series('ICSA', period, frequency='w', units=units)

    def get_unemployment(self, period='1Y', units='pc1'):
        return self._fetch_series('UNRATE', period, frequency='m', units=units)

    def get_industrial_production(self, period='1Y', units='pc1'):
        return self._fetch_series('INDPRO', period, frequency='m', units=units)

    def get_net_exports(self, period='1Y', units='lin'):
        return self._fetch_series('NETEXC', period, frequency='q', units=units)        

