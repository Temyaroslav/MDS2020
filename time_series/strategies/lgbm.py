import numpy as np
import optuna.integration.lightgbm as lgb
from sklearn.model_selection import train_test_split

from . import BaseStrategy


class StrategyLGBM(BaseStrategy):
    '''Light GBM strategy class'''
    def __init__(self, params: dict):
        super().__init__()
        self.fitted_model = None
        self.params = params
        self._rounds = 1000

    def fit(self, X):
        # target is actually t+1, so we need get rid of the last observation to avoid forward looking bias
        X = X.iloc[:-1, :]
        # separate the last month of data into validation (assuming 3h candles)
        X_train, X_val = X.iloc[:-20*3, :], X.iloc[-20*3:, :]
        dtrain = lgb.Dataset(X_train.drop(['Date', 'target'], axis=1), label=X_train['target'])
        dval = lgb.Dataset(X_val.drop(['Date', 'target'], axis=1), label=X_val['target'])
        # tune the model
        self.fitted_model = lgb.train(self.params, dtrain, verbose_eval=False,
                                      num_boost_round=self._rounds, valid_sets=dval)
        
    def predict(self, X=None):
        # taking only the last observation to make t+1 prediction
        X = X.iloc[-1, :]
        # excluding the target which we need to predict
        X = X.drop(['Date', 'target'])
        pred = self.fitted_model.predict(np.array(X).reshape(1, -1))
        return -1 if round(pred[0]) == 0 else round(pred[0])
