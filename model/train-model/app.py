import numpy as np
import pandas as pd

path = '/content/vehicle_prediction.csv'
data = pd.read_csv(path, encoding='latin-1')

data.head()

data.shape

data.isnull()

data.isnull().sum()

data.info()

data.head(2)

data.corr()['selling_price']

len(data['brand'].value_counts())

def add_brand(inpt):
    if inpt == 'Aston' or inpt == 'Scion' or inpt == 'McLaren' or inpt == 'Saturn' or inpt == 'FIAT' or inpt == 'Lotus' or inpt == 'Mercury' or inpt == 'Lucid' or inpt == 'Saab' or inpt == 'Karma' or inpt == 'Bugatti' or inpt == 'smart' or inpt == 'Suzuki' or inpt == 'Maybach' or inpt == 'Plymouth' or inpt == 'Polestar':
        return 'Other'
    else:
        return inpt

data['brand'] = data['brand'].apply(add_brand)

data['brand'].value_counts()

len(data['brand'].value_counts())

data['model'].value_counts()

data['model'].value_counts().head(20)

def add_model(inpt):
    if inpt == 'M3 Base' or inpt == 'F-150 XLT' or inpt == 'Corvette Base' or inpt == '1500 Laramie' or inpt == 'Wrangler Sport' or inpt == 'Camaro 2SS' or inpt == 'Model Y Long Range' or inpt == 'Mustang GT Premium' or inpt == '911 Carrera' or inpt == 'M4 Base' or inpt == 'Explorer XLT' or inpt == 'F-250 Lariat' or inpt == '911 Carrera S' or inpt == 'M5 Base' or inpt == 'E-Class E 350 4MATIC' or inpt == 'E-Class E 350'  or inpt == 'F-150 Lariat' or inpt == 'ES 350 Base' or inpt == 'R1S Adventure Package' or inpt == 'F-250 XLT':
        return inpt
    else:
        return 'Other'

data['model'] = data['model'].apply(add_model)

data['model'].value_counts()

len(data['model'].value_counts())

data['fuel_type'].value_counts()

data['engine'].value_counts()

data['engine'].value_counts().head(20)

def add_engine(inpt):
    if inpt == '835.0HP Electric Motor Electric Fuel System' or inpt == '2.0L I4 16V GDI DOHC Turbo' or inpt == '355.0HP 5.3L 8 Cylinder Engine Gasoline Fuel' or inpt == '420.0HP 6.2L 8 Cylinder Engine Gasoline Fuel' or inpt == '300.0HP 3.0L Straight 6 Cylinder Engine Gasoline Fuel' or inpt == '240.0HP 2.0L 4 Cylinder Engine Gasoline Fuel' or inpt == '285.0HP 3.6L V6 Cylinder Engine Gasoline Fuel' or inpt == '5.7L V8 16V MPFI OHV' or inpt == '340.0HP 3.0L V6 Cylinder Engine Gasoline Fuel' or inpt == '3.6L V6 24V MPFI DOHC' or inpt == '3.6L V6 24V GDI DOHC' or inpt == '455.0HP 6.2L 8 Cylinder Engine Gasoline Fuel' or inpt == '268.0HP 3.5L V6 Cylinder Engine Gasoline Fuel' or inpt == '302.0HP 3.5L V6 Cylinder Engine Gasoline Fuel' or inpt == '490.0HP 6.2L 8 Cylinder Engine Gasoline Fuel' or inpt == '295.0HP 3.5L V6 Cylinder Engine Gasoline Fuel'  or inpt == '445.0HP 4.4L 8 Cylinder Engine Gasoline Fuel' or inpt == '3.5L V6 24V PDI DOHC Twin Turbo' or inpt == '4.0L V8 32V GDI DOHC Twin Turbo' or inpt == '425.0HP 3.0L Straight 6 Cylinder Engine Gasoline Fuel':
        return inpt
    else:
        return 'Other'

data['engine'] = data['engine'].apply(add_engine)

data['engine'].value_counts()

len(data['engine'].value_counts())

data['transmission'].value_counts()

data['transmission'].value_counts().head(20)

def add_transmission(inpt):
    if inpt == 'A/T' or inpt == '8-Speed A/T' or inpt == 'Transmission w/Dual Shift Mode' or inpt == '6-Speed A/T' or inpt == '6-Speed M/T' or inpt == 'Automatic' or inpt == '7-Speed A/T' or inpt == '8-Speed Automatic' or inpt == '10-Speed A/T' or inpt == '5-Speed A/T' or inpt == '9-Speed A/T' or inpt == '6-Speed Automatic' or inpt == '4-Speed A/T' or inpt == '1-Speed A/T' or inpt == 'CVT Transmission' or inpt == '5-Speed M/T'  or inpt == '10-Speed Automatic' or inpt == '9-Speed Automatic' or inpt == 'M/T' or inpt == 'Automatic CVT':
        return inpt
    else:
        return 'Other'

data['transmission'] = data['transmission'].apply(add_transmission)

data['transmission'].value_counts()

data.info()

data.head(2)

data = data.drop(columns=['milage', 'ext_col', 'int_col', 'accident', 'clean_title', 'price'])

data.head(2)

data = pd.get_dummies(data)

data.head(2)

data.shape

X = data.drop('selling_price', axis=1)
y = data['selling_price']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

X_train.shape, X_test.shape

def model_acc(model):
  model.fit(X_train, y_train)
  acc = model.score(X_test, y_test)
  print(str(model) + ' --> ' + str(acc))


from sklearn.linear_model import LinearRegression
lr = LinearRegression()
model_acc(lr)

from sklearn.linear_model import Lasso
lasso = Lasso()
model_acc(lasso)

from sklearn.tree import DecisionTreeRegressor
dt = DecisionTreeRegressor()
model_acc(dt)

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
model_acc(rf)

from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators':[10, 50, 100],
              'criterion':['squared_error','absolute_error','poisson']}

grid_obj = GridSearchCV(estimator=rf, param_grid=parameters)

grid_fit = grid_obj.fit(X_train, y_train)

best_model = grid_fit.best_estimator_

best_model

best_model.score(X_test, y_test)

import pickle
with open('predictor.pickle', 'wb') as file:
    pickle.dump(best_model, file)

X_train.columns

pred_value = best_model.predict([[
55000, 2022, 0, 0, 0, 0, 0, 1, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
0, 0
]])
pred_value

