import pickle
from tqdm import tqdm

import numpy as np
import pandas as pd

from loaders import DataLoader
from strategies import BaseStrategy
from strategies.arima import StrategyARIMA, StrategyARIMAGARCH

import warnings
warnings.filterwarnings('ignore')


class BackTester:
    def __init__(self,
                 data: pd.DataFrame,
                 strategy: BaseStrategy,
                 window: int,
                 refit_window):
        '''
            data: data for backtesting
            strategy: strategy class to backtest
            window: time window on which to fit the strategy
        '''
        self.data = data
        self.strategy = strategy
        self.window, self.refit_window = window, refit_window

    def run(self):
        '''main method to iterate over the data and store predictions'''
        # in this way t+1 prediction will be stored in the same row as t+1 observation making it convenient to calculate Pnl
        predictions = [np.nan] * self.window
        for i, idx in enumerate(tqdm(range(self.data.shape[0] - self.window))):
            # slice the window
            X = self.data.iloc[idx:idx + self.window, :]
            try:
                # check if it is time to refit
                if idx == 0:
                    self.strategy.fit(X)
                else:
                    if X['state'].iloc[-1] == 1 and X['Date'].iloc[-1].isocalendar().week != X['Date'].iloc[
                        -2].isocalendar().week:
                        self.strategy.fit(X)
                # make one step prediction
                pred = self.strategy.predict(X)
                predictions.append(pred)
            except Exception as e:
                print(e)
                predictions.append(1.0)

        self.data['Pred'] = predictions

        # cache results
        with open(f'{self.strategy.__class__.__name__}_{self.window}_{self.refit_window}.pkl', 'wb') as f:
            pickle.dump(self.data, f)
        print(f'{self.strategy.__class__.__name__}_{self.window}_{self.refit_window}.pkl is cached.')


with open('HMM2.pkl', 'rb') as f:
    df_hmm = pickle.load(f)

df = DataLoader.load('ibm', sampling='3H', year_start=2000)

df['tmp'] = df['Date'].apply(lambda x: f'{x.year}_{x.isocalendar().week}')
df['state'] = df['tmp'].map(dict(zip(df_hmm['Date_id'], df_hmm['state'])))
df.drop(['tmp'], axis=1, inplace=True)
df.fillna(value=0, inplace=True)

strategy = StrategyARIMAGARCH()

backtester = BackTester(data=df,
                        strategy=strategy,
                        window=3*252*3, refit_window='HMM2')

backtester.run()
