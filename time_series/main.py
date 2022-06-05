import json
import warnings

import pandas as pd
from sklearn.model_selection import train_test_split

from loaders import DataLoader
from backtester import BackTester

from strategies.lgbm import StrategyLGBM
from strategies.ensemble import StrategyEnsemble
from strategies.arima import StrategyARIMA, StrategyARIMAGARCH
from strategies.hmm import StrategyHMM


def main():
    df = DataLoader.load('ibm', sampling='3H', year_start=2000)
    # X_train, X_test, _, _ = train_test_split(df, df['target'], test_size=0.2, shuffle=False)

    window = 3*252*5
    # df_test = pd.concat([X_train.iloc[-window:, :], X_test])

    with open('lgbm_param.json', 'r') as f:
        best_params = json.load(f)
    best_params.update({
        "objective": "binary",
        "metric": "binary_error",
        "verbosity": -1,
        "boosting_type": "gbdt",
        "seed": 42})

    # strategy = StrategyARIMA()
    strategy = StrategyARIMAGARCH()
    # strategy = StrategyLGBM(best_params)
    # strategy = StrategyEnsemble(models=['StrategyARIMA_1512_756.pkl', 'StrategyARIMAGARCH_1512_756.pkl',
    #                                     'StrategyLGBM_3780_378.pkl', 'StrategyLGBM_3780_756.pkl'])

    backtester = BackTester(data=df,
                            strategy=strategy,
                            window=3*252*3,
                            refit_window=15)
    backtester.run()
    # backtester.plot_pnl(False, 'StrategyARIMA_1512_756.pkl')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    main()