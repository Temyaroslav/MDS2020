import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

from . import BaseStrategy


class StrategyEnsemble(BaseStrategy):
    '''Ensemble strategy class'''

    def __init__(self, models: list):
        super().__init__()
        # collect predictions from cached models
        self.cached_preds = None
        for idx, model in enumerate(models):
            with open(model, 'rb') as f:
                ff = pickle.load(f)
            # check if predictions are in binary format
            if len(set(ff['Pred'].values)) != 2:
                ff['Pred'] = np.sign(ff['Pred'])
            if self.cached_preds is None:
                self.cached_preds = ff[['Date', 'Pred']]
                self.cached_preds.rename(columns={'Pred': 'Pred_0'}, inplace=True)
                continue
            self.cached_preds[f'Pred_{idx}'] = self.cached_preds['Date'].map(dict(zip(ff['Date'], ff['Pred'])))
        del ff
        self.cached_preds.dropna(inplace=True)
        # placeholder for ensemble classifier
        self.model = LogisticRegression()

    def fit(self, X):
        # target is actually t+1, so we need get rid of the last observation to avoid forward looking bias
        X = X.iloc[:-1, :]
        X_train = self.cached_preds[self.cached_preds['Date'].isin(X['Date'])]
        self.model.fit(X_train.drop('Date', axis=1), X['target'])

    def predict(self, X=None):
        # taking only the last observation to make t+1 prediction
        X = X.iloc[-1, :]
        # take the cached predictions from other models
        preds = self.cached_preds[self.cached_preds['Date'] == X['Date']]
        # pass them to the ensemble to make the prediction
        pred = self.model.predict(preds.drop('Date', axis=1))

        return pred[0]