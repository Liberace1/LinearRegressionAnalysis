# -*- coding: utf-8 -*-
"""LinearRegressionAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dzATgcflFyDaSGxlrz53NcMWRZsuBuTu
"""

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score

url = 'https://drive.google.com/uc?id=1pDY_86K06c7b1QpRC-yOiifPxUzxl5oV'
df = pd.read_csv(url)
df.head()

df.info()

features = ["housing_median_age",	"total_rooms",	"total_bedrooms",
            "population", "households",	"median_income",	"median_house_value",
            "ocean_proximity"]

sns.pairplot(df[features], hue="ocean_proximity")

sns.histplot(df["housing_median_age"])

sns.histplot(df["median_income"])

sns.histplot(df["median_house_value"])

selected_features = ["housing_median_age", 'median_income', 'median_house_value']
X = df[["housing_median_age", 'median_income']]
y = df['median_house_value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

lr_r2 = r2_score(y_test, y_pred)
lr_rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)))

print("Linear Regression: R2", lr_r2)
print("Linear Regression: RMSE", lr_rmse)

parameters = {"alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
              "fit_intercept": [True, False],
              "penalty": ['l2', 'l1', 'elasticnet', None],
              "learning_rate": ['constant', 'optimal',
                                'invscaling', 'adaptive']
             }
sgdr = SGDRegressor();
grid = GridSearchCV(estimator=sgdr, param_grid = parameters, cv = 2, n_jobs=-1)
grid.fit(X_train, y_train)

sgdr = SGDRegressor(**grid.best_params_)
sgdr.fit(X_train, y_train)
y_pred = sgdr.predict(X_test)

sgdr_r2 = r2_score(y_test, y_pred)
sgdr_rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)))

print("SGDRegressor: R2", sgdr_r2)
print("SGDRegressor: RMSE", sgdr_rmse)