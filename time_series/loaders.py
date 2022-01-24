import os
import pandas as pd


class DataLoader:
    @classmethod
    def load(cls, asset: str,
             sampling: str = '1H',
             year_start: int = 2000,
             year_end: int = None):
        if os.path.exists(f'{asset}.csv'):
            data = pd.read_csv(f'{asset}.csv', header=None)
        else:
            raise FileNotFoundError('{asset}.csv was not found!')
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data.iloc[:, 1:-1] /= 10e3
        data['Date'] = pd.to_datetime(data['Date'])
        if year_end is None:
            year_end = data['Date'].dt.year.unique()[-1]
        data = data[(data['Date'].dt.year >= year_start) & (data['Date'].dt.year <= year_end)]
        data.reset_index(inplace=True, drop=True)
        if sampling != '1H':
            data = cls._resample(data, sampling)
        return data

    @staticmethod
    def _resample(data: pd.DataFrame, sampling):
        data.set_index('Date', inplace=True)
        data = data.resample(sampling).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last'})
        data.dropna(inplace=True)
        data.reset_index(inplace=True)
        return data