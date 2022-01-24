from itertools import product
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import arch

from . import BaseStrategy


class StrategyARIMA(BaseStrategy):
    def __init__(self, max_p: int = 5, max_q: int = 5):
        super().__init__()
        self.max_p, self.max_q = max_p, max_q
        self.params = None

    def fit(self, X):
        xs = X['ln_Close'].values
        final_aic = np.inf
        parameters = list(product(range(5), range(5)))
        for param in parameters:
            if param[0] == param[1] == 0:
                continue
            try:
                model = ARIMA(xs, order=(param[0], 0, param[1])).fit()
            except ValueError:
                continue
            if model.aic < final_aic:
                final_aic = model.aic
                #                 self.model = deepcopy(model)
                self.params = param

    def predict(self, X=None):
        xs = X['ln_Close'].values
        model = ARIMA(xs, order=(self.params[0], 0, self.params[1])).fit()
        pred = model.forecast(steps=1)[0]
        return pred


class StrategyARIMAGARCH(BaseStrategy):
    '''ARIMA+GARCH strategy class'''
    def __init__(self, max_p: int = 5, max_q: int = 5):
        super().__init__()
        self.max_p, self.max_q = max_p, max_q
        self.params = None
    
    def fit(self, X):
        '''
            Calculates ARIMA parameters by minimizing Akaike Information Criterion and stores the best combination.
        '''
        xs = X['ln_Close'].values
        final_aic = np.inf
        parameters = list(product(range(5), range(5)))
        for param in parameters:
            if param[0] == param[1] == 0:
                continue
            try:
                model = ARIMA(xs, order=(param[0], 0, param[1])).fit()
            except ValueError:
                continue
            if model.aic < final_aic:
                final_aic = model.aic
                self.params = param
                
    def predict(self, X=None):
        '''
            To predict the next value we first fit ARIMA with optimised set of parameters.
            Then we fit GARCH using ARIMA's residuals and combine the prediction of ARIMA+GARCH models.
        '''
        xs = X['ln_Close'].values
        arima = ARIMA(xs, order=(self.params[0], 0, self.params[1])).fit()
        arima_pred = arima.forecast(steps=1)[0]
        
        garch = arch.arch_model(arima.resid)
        garch_fit = garch.fit(disp='off', show_warning=False)
        garch_pred = garch_fit.forecast(horizon=1).mean.iloc[-1]['h.1']
        
        pred = arima_pred + garch_pred
        
        return pred