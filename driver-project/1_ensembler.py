# Common imports
import numpy as np
import os

# Constant seed
np.random.seed(42)

import pandas as pd

DATA_PATH='./data'


# In[4]:


train = pd.read_csv(os.path.join(DATA_PATH, "train.csv"))
test = pd.read_csv(os.path.join(DATA_PATH, "test.csv"))


# For scikit-learn models
cols = [x for x in range(3,60)]
cols_final = [x for x in range(1,58)]
x_train= pd.read_csv(os.path.join(DATA_PATH, "train_subset.csv"), usecols=cols)
y_train = pd.read_csv(os.path.join(DATA_PATH, "train_subset.csv"), usecols=[2])

x_test= pd.read_csv(os.path.join(DATA_PATH, "test_subset.csv"), usecols=cols)
y_test = pd.read_csv(os.path.join(DATA_PATH, "test_subset.csv"), usecols=[2])

x_final = pd.read_csv(os.path.join(DATA_PATH, "test.csv"), usecols=cols_final)


# calculate gini, ref: http://shichaoji.com/tag/train-model-predictive-insurance-auto-claim-gini-scikit-learn/
def gini(y_true, y_pred):
    # check and get number of samples
    assert y_true.shape == y_pred.shape
    n_samples = y_true.shape[0]
    
    # sort rows on prediction column 
    # (from largest to smallest)
    arr = np.array([y_true, y_pred]).transpose()
    true_order = arr[arr[:,0].argsort()][::-1,0]
    pred_order = arr[arr[:,1].argsort()][::-1,0]
    
    # get Lorenz curves
    L_true = np.cumsum(true_order) / np.sum(true_order)
    L_pred = np.cumsum(pred_order) / np.sum(pred_order)
    L_ones = np.linspace(1/n_samples, 1, n_samples)
    
    # get Gini coefficients (area between curves)
    G_true = np.sum(L_ones - L_true)
    G_pred = np.sum(L_ones - L_pred)
    
    # normalize to true Gini coefficient
    return G_pred/G_true


from sklearn.metrics import accuracy_score

from xgboost import XGBRegressor


# ### XGBoost Training

# apply xgboost
# ref: http://shichaoji.com/tag/train-model-predictive-insurance-auto-claim-gini-scikit-learn/
import xgboost as xgb
d_train = xgb.DMatrix(x_train, y_train)
d_valid = xgb.DMatrix(x_test, y_test)
d_test = xgb.DMatrix(x_test)

def use_gini(a, b):
    y = b.get_label()
    return 'gini', gini(y, a)
    
watchlist = [(d_train, 'train'), (d_valid, 'valid')]

xgb_reg = xgb.Booster()
xgb_reg.load_model(os.path.join('xgboost_models','xgb_2.bst'))
d_final = xgb.DMatrix(x_final)

y_xgb = xgb_reg.predict(d_final)
print('XGB Done.')


# Catboost
from catboost import CatBoostRegressor

cat_reg = CatBoostRegressor()
cat_reg.load_model(os.path.join('catboost_models','cat_1.bst'))
y_cat = cat_reg.predict(x_final)
print('Catboost Done.')

# LightGBM

import lightgbm as lgb

lgb_params = {}
lgb_params['learning_rate'] = 0.05
lgb_params['n_estimators'] = 500
lgb_params['max_depth'] = 4
lgb_params['seed'] = 42
lgb_params['metric'] = 'auc'

train_data = lgb.Dataset(x_train, label=y_train.values.ravel())
test_data = lgb.Dataset(x_test, label=y_test.squeeze())

lgb_reg = lgb.Booster(model_file='lgb_models/lgb_1.txt') 
y_lgb = lgb_reg.predict(x_final)

print('LightGBM Done.')

y_output = (y_xgb+y_cat+y_lgb)/3

id_test = test['id'].values
sub = pd.DataFrame()
sub['id'] = id_test
sub['target'] = y_output
sub.to_csv('submissions/submission_3.csv', index=False)