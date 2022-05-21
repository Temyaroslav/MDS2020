from tqdm import tqdm
import pickle
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, f1_score
from strategies import BaseStrategy


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
            refit_window: how often we refit the strategy
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
            # check if it is time to refit
            if type(self.refit_window) is int:
                if i % self.refit_window == 0:
                    self.strategy.fit(X)
            else:
                self.refit_window.fit(X)
                refit_signal = self.refit_window.predict(X)
                if refit_signal:
                    self.strategy.fit(X)
            # make one step prediction
            pred = self.strategy.predict(X)
            predictions.append(pred)
        
        self.data['Pred'] = predictions
        
        # cache results
        with open(f'{self.strategy.__class__.__name__}_{self.window}_{self.refit_window}.pkl', 'wb') as f:
            pickle.dump(self.data, f)
        print(f'{self.strategy.__class__.__name__}_{self.window}_{self.refit_window}.pkl is cached.')
            
    def plot_pnl(self, is_binary_prediction: bool, cache_path=None):
        if cache_path is not None:
            with open(cache_path, 'rb') as f:
                self.data = pickle.load(f)
        # get rid of nans
        data = self.data.copy().dropna()
        
        if not is_binary_prediction:
            # transform the predictions from the log changes to the binary format by taking the sign
            data['Pred'] = np.sign(data['Pred'])
        
        plt.figure(figsize=(10, 8))
        # plot buy&hold benchmark
        plt.plot(data['Date'], data['Close'].diff().cumsum(), c='red', label='Buy&Hold')
        plt.plot(data['Date'], data['Close'].diff().mul(data['Pred']).cumsum(), c='C0', label=self.strategy.__class__.__name__)
        plt.grid()
        plt.legend()
        plt.title('PnL results')
        plt.show()
        
        # run some metrics
        y_pred = data['Pred']
        y_true = np.sign(data['ln_Close'])
        # due to the nature of our data (only 2 decimal points) there are few occasions when close price is unchanged
        # applying a small tweak to make our target and prediction binary
        y_true[y_true == 0] = 1.0
        y_pred[y_pred == 0] = 1.0
        print(f'Accuracy: {accuracy_score(y_true, y_pred)}')
        print(f'f1: {f1_score(y_true, y_pred)}')
