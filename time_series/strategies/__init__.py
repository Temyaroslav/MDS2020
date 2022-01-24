class BaseStrategy:
    def fit(self, X):
        raise NotImplementedError

    def predict(self, X=None):
        raise NotImplementedError
