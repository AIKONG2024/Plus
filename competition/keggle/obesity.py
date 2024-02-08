# https://www.kaggle.com/competitions/playground-series-s4e2
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold, cross_val_score ,StratifiedKFold, cross_val_predict , GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import lightgbm as lgbm
import xgboost as xgb
import catboost as cbst
import sys
import time
sys.path.append('C:/MyPackages/')
from keras_custom_pk.file_name import *


path = "C:/_data/kaggle/obesity/"
# ====================================================
# 데이터 가져오기
train_csv = pd.read_csv(path + "train.csv", index_col=0)
test_csv = pd.read_csv(path + "test.csv", index_col=0)
submission_csv = pd.read_csv(path + "sample_submission.csv")
# ====================================================
# 수치화 : Gender, family_history_with_overweight, FAVC, CAEC, SMOKE, SCC, CALC, MTRANS,NObeyesdad
lbe = LabelEncoder()
train_csv['Gender'] = lbe.fit_transform(train_csv['Gender'])
test_csv['Gender'] = lbe.transform(test_csv['Gender'])

train_csv['family_history_with_overweight'] = lbe.fit_transform(train_csv['family_history_with_overweight'])
test_csv['family_history_with_overweight'] = lbe.transform(test_csv['family_history_with_overweight'])

train_csv['FAVC'] = lbe.fit_transform(train_csv['FAVC'])
test_csv['FAVC'] = lbe.transform(test_csv['FAVC'])

train_csv['CAEC'] = lbe.fit_transform(train_csv['CAEC'])
test_csv['CAEC'] = lbe.transform(test_csv['CAEC'])

train_csv['SMOKE'] = lbe.fit_transform(train_csv['SMOKE'])
test_csv['SMOKE'] = lbe.transform(test_csv['SMOKE'])

train_csv['SCC'] = lbe.fit_transform(train_csv['SCC'])
test_csv['SCC'] = lbe.transform(test_csv['SCC'])

train_csv['CALC'] = lbe.fit_transform(train_csv['CALC'])
if 'Always' not in lbe.classes_:
    lbe.classes_ = np.append(lbe.classes_, 'Always') 
test_csv['CALC'] = lbe.transform(test_csv['CALC'])

train_csv['MTRANS'] = lbe.fit_transform(train_csv['MTRANS'])
test_csv['MTRANS'] = lbe.transform(test_csv['MTRANS'])

train_csv['NObeyesdad'] = lbe.fit_transform(train_csv['NObeyesdad'])

# 뽑아낼값 : [NObeyesdad]
x = train_csv.drop(['NObeyesdad'], axis=1)
y = train_csv['NObeyesdad']

print(x.shape, y.shape) #(20758, 16) (20758,)

#데이터
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state= 100)

x_train, x_test, y_train, y_test = train_test_split(x,y,shuffle=True, random_state=123, train_size=0.8, stratify=y)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
test_csv = scaler.transform(test_csv)

# n_splits = 3
# kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=123)

parameters = [
    {"max_depth": [10]},
    # {"learning_rate": [1e-2, 1e-3, 1e-4], "best_model_min_trees": [3, 5, 7, 9, 11], "max_depth": [10, 20], "max_leaves" : [6, 10 ,15]},
    # {"learning_rate": [1e-2, 1e-3, 1e-4], "best_model_min_trees": [3, 5, 7, 9, 11], "max_depth": [10, 20]},
]

# ====================================================
#모델 구성
# model = RandomForestClassifier()
# model = lgbm.LGBMClassifier()
model = cbst.CatBoostClassifier()
# model = xgb.XGBClassifier()

# gsc = GridSearchCV(model, param_grid= parameters , cv=kf, n_jobs=-1, refit=True, verbose=1 )
# gsc.fit(x_train, y_train) 
# x_pred = gsc.best_estimator_.predict(x_test)
# best_acc_score = accuracy_score(y_test, x_pred) 
# print("best_acc_score : ", best_acc_score)
# submission = gsc.best_estimator_.predict(test_csv)
model.fit(x_train, y_train)
submission = lbe.inverse_transform(model.predict(test_csv)) 
# ====================================================
# 데이터 저장 
submission_csv["NObeyesdad"] = submission
file_name = csv_file_name(path, f"obesity_submit_")
submission_csv.to_csv(file_name, index=False)
# h5_file_name_d = h5_file_name(path, f"obesity_submit_")
# model.save(h5_file_name_d)

'''
[RandomForestClassifier] : [0.90004817 0.90197495 0.89908478 0.89327873 0.89906047]
[LGBMClassifier] : [0.90366089 0.9077553  0.90968208 0.89978318 0.90267405]
[CatBoostClassifier] : [0.90414258 0.90944123 0.9072736  0.90315587 0.90676945]
[XGBClassifier] : [0.90293834 0.90871869 0.90486513 0.90243315 0.90676945]
'''