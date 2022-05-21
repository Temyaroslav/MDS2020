from hmmlearn.hmm import GaussianHMM

from . import BaseStrategy


class StrategyHMM(BaseStrategy):
    '''Hidden Markov Model strategy class'''
    def __init__(self, n_components):
        super().__init__()
        self.hmm_model = GaussianHMM(n_components=n_components,
                                     covariance_type="full",
                                     n_iter=1000,
                                     # init_params='ste'
                                     )
        self._previous_state = -99

    def fit(self, X):
        rets = X['ln_Close'].to_numpy().reshape(-1, 1)        
        self.hmm_model.fit(rets)
        
    def predict(self, X=None):
        rets = X['ln_Close'].to_numpy().reshape(-1, 1)
        hidden_state = self.hmm_model.predict(rets)[-1]
        if hidden_state == self._previous_state:
            return 0
        else:
            self._previous_state = hidden_state
            return 1

    def __str__(self):
        return f'HMM{self.hmm_model.n_components}'