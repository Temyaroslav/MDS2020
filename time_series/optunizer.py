import json
import pickle

import optuna.integration.lightgbm as lgb
import optuna
import pandas as pd
from sklearn.model_selection import train_test_split

from splitting import PurgedGroupTimeSeriesSplit
from loaders import DataLoader


def objective(trial):
    '''main method for optuna tuning hyperparameters'''
    param = {
        'objective': 'binary',
        'metric': 'binary_error',
        'lambda_l1': trial.suggest_loguniform('lambda_l1', 1e-8, 10.0),
        'lambda_l2': trial.suggest_loguniform('lambda_l2', 1e-8, 10.0),
        'num_leaves': trial.suggest_int('num_leaves', 2, 512),
        'feature_fraction': trial.suggest_uniform('feature_fraction', 0.1, 1.0),
        'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.1, 1.0),
        'bagging_freq': trial.suggest_int('bagging_freq', 0, 15),
        'min_child_samples': trial.suggest_int('min_child_samples', 1, 100),
        'seed': 42,
        'verbosity': -1,
        'boosting_type': 'gbdt',
        "feature_pre_filter": False
    }

    lgbcv = lgb.cv(param,
                   dtrain,
                   folds=cv.split(X=X_train, y=y_train, groups=groups),
                   verbose_eval=False,
                   early_stopping_rounds=250,
                   num_boost_round=10000,
                   callbacks=[lgb.reset_parameter(learning_rate=[0.005] * 200 + [0.001] * 9800)]
                   )

    cv_score = lgbcv['binary_error-mean'][-1] + lgbcv['binary_error-stdv'][-1]

    return cv_score


df = DataLoader.load('ibm_trainval', sampling='3H')
df_1h = DataLoader.load('ibm_trainval', sampling='1H')
df_1d = DataLoader.load('ibm_trainval', sampling='1D')
df_1h.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'target'], axis=1, inplace=True)
df_1d.drop(['Open', 'High', 'Low', 'Close', 'target'], axis=1, inplace=True)
df_1h.columns = [x + '_1H' for x in df_1h.columns]
df_1d.columns = [x + '_1D' for x in df_1d.columns]
df = df.merge(df_1h, left_on='Date', right_on='Date_1H')
df.drop(['Date_1H'], axis=1, inplace=True)
df['tmp'] = df['Date'].dt.date.astype('datetime64')
df = df.merge(df_1d, left_on='tmp', right_on='Date_1D')
df.drop(['tmp', 'Date_1D'], axis=1, inplace=True)
del df_1h, df_1d

X_train, X_test, y_train, y_test = train_test_split(df.drop('target', axis=1), df['target'], test_size=0.2,
                                                    shuffle=False)
dtrain = lgb.Dataset(X_train.drop('Date', axis=1), label=y_train)
groups = pd.factorize(X_train['Date'].dt.day.astype(str) + '_' + \
                      X_train['Date'].dt.month.astype(str) + '_' + \
                      X_train['Date'].dt.year.astype(str))[0]
cv = PurgedGroupTimeSeriesSplit(n_splits=3, group_gap=20*3, max_train_group_size=252*3*3,
                                max_test_group_size=252*3)
optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction='minimize')
study.optimize(objective, timeout=10800)

print('Number of finished trials:', len(study.trials))
print('Best trial:', study.best_trial.params)

# saving the best hyperparameters values
with open('lgbm_param_extended.json', 'w') as f:
    json.dump(study.best_trial.params, f)

# saving the study
with open('lgbm_optuna_study.pkl', 'wb') as f:
    pickle.dump(study, f)
