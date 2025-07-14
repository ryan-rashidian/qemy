import matplotlib.pyplot as plt
import pandas as pd

from qemy import _config as cfg
from qemy.data import FREDClient
from qemy.utils.file_tools import save_to_png


class PlotFRED:
    def __init__(self):
        self.export_dir = cfg.EXPORT_CHART_DIR

    def _plot(
        self,
        fred_func,
        period,
        units,
        label,
        title,
        y_label,
        filename,
        save
    ):
        fred_data = fred_func(period=period, units=units)
        fred_df = pd.DataFrame(fred_data)

        plt.figure(figsize=(14, 8))
        plt.plot(
            fred_df.index,
            fred_df['val'],
            label=label,
            color='green',
            linewidth=3,
            marker= 'o',
            alpha=0.8
        )
        plt.xlabel('Date')
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if save:
            save_to_png(filename=filename)
        plt.show()

    def plot_cpi(self, period, save=False, units='pc1'):
        self._plot(
            fred_func=FREDClient().get_cpi,
            period=period, units=units,
            label="CPI Inflation",
            title=f"CPI Inflation: {units}",
            y_label="Inflation",
            filename="cpichart",
            save=save
        )

    def plot_gdp(self, period, save=False, units='pc1'):
        self._plot(
            fred_func=FREDClient().get_gdp,
            period=period, units=units,
            label="Gross Domestic Product",
            title=f"Gross Domestic Product: {units}",
            y_label="GDP",
            filename="gdpchart",
            save=save
        )

    def plot_sentiment(self, period, save=False, units='pch'):
        self._plot(
            fred_func=FREDClient().get_sentiment,
            period=period, units=units,
            label="Consumer Sentiment Index",
            title=f"Consumer Sentiment Index: {units}",
            y_label="Sentiment",
            filename="sentchart",
            save=save
        )

    def plot_nfp(self, period, save=False, units='pc1'):
        self._plot(
            fred_func=FREDClient().get_nf_payrolls,
            period=period, units=units,
            label="Nonfarm Payrolls",
            title=f"Nonfarm Payrolls: {units}",
            y_label="nfp",
            filename="nfpchart",
            save=save
        )

    def plot_interest(self, period, save=False, units='pc1'):
        self._plot(
            fred_func=FREDClient().get_interest_rate,
            period=period, units=units,
            label="Fed Interest Rate",
            title=f"Fed Interest Rate: {units}",
            y_label="interest",
            filename="interestchart",
            save=save
        )

    def plot_jobc(self, period, save=False, units='pc1'):
        self._plot(
            fred_func=FREDClient().get_jobless_claims,
            period=period, units=units,
            label="Jobless Claims",
            title=f"Jobless Claims: {units}",
            y_label="jobc",
            filename="jobcchart",
            save=save
        )

    def plot_unem(self, period, save=False, units='pc1'):
        self._plot(
            fred_func=FREDClient().get_unemployment,
            period=period, units=units,
            label="Unemployment Rate",
            title=f"Unemployment Rate: {units}",
            y_label="unem",
            filename="unemchart",
            save=save
        )

    def plot_indp(self, period, save=False, units='pc1'):
        self._plot(
            fred_func=FREDClient().get_industrial_production,
            period=period, units=units,
            label="Industrial Production",
            title=f"Industrial Production: {units}",
            y_label="indp",
            filename="indpchart",
            save=save
        )

    def plot_netex(self, period, save=False, units='lin'):
        self._plot(
            fred_func=FREDClient().get_net_exports,
            period=period, units=units,
            label="Net Exports",
            title=f"Net Exports: {units}",
            y_label="netex",
            filename="netexchart",
            save=save
        )

