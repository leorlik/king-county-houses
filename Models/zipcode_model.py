from sklearn import linear_model, preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import sqlite3
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from sklearn import svm
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures

PATH_TO_DATABASE = '../data/kc_house_data.db'

def read_from_db():

    # Connect to the SQLite database
    conn = sqlite3.connect(PATH_TO_DATABASE)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Read the data from the database
    data = pd.read_sql_query("SELECT * FROM sales_variables LEFT JOIN house_variables ON sales_variables.id = house_variables.id", conn)

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    return data

def main():

    # Load the data
    data = read_from_db()

    # Dropping the log cause we'll use Standard Scaler
    X = data.drop(['price', 'lat', 'long', 'sales_date', 'id', 'yr_renovated',
                   'log_living', 'log_living15', 'log_lot', 'log_lot15','log_above', 'log_basement'], axis=1).fillna(0)
    y = data['price']

    X['zipcode'] = X['zipcode'].astype("str")
    X = pd.get_dummies(X,columns=['zipcode'],drop_first=True)

    lbl = LabelEncoder()
    X['season'] = lbl.fit_transform(X['season'])
    X['better_view'] = lbl.fit_transform(X['better_view'])
    o_e = OrdinalEncoder()
    X['yr_built'] = o_e.fit_transform(X[['yr_built']])

    # Create the training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size=0.2, random_state=98)
    
    ## Using only these cause were far better in the other approach
    regressors = {
        'Linear': linear_model.LinearRegression(),
        'RandomForest': RandomForestRegressor(),
    }

    params = {
        'Linear': {'clf__fit_intercept': [True, False],
                   'ply__degree': [1, 2]},
        'RandomForest': {'clf__n_estimators': [10, 100, 1000], 'clf__max_features': ['auto', 'sqrt', 'log2'],
                         'ply__degree': [1]}
    }

    rgsrs = {}
    results = {}

    for model in regressors.keys():
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('ply', PolynomialFeatures()),
            ('clf', regressors[model])
        ]   )
        gs = GridSearchCV(pipe, params[model], cv=5)
        gs.fit(X_train, y_train)
        y_pred = gs.predict(X_test)
        rgsrs[model] = gs
        results[model] = gs.best_score_
        print(f'{model} best score: {gs.best_score_}')
        print(f'{model} best params: {gs.best_params_}')
        print(f'{model} MAE: {mean_absolute_error(y_test, y_pred)}')
        print(f'{model} MSE: {mean_squared_error(y_test, y_pred)}')
        print(f'{model} R2: {r2_score(y_test, y_pred)}')

    ## Saving the model
    best_model = max(results, key=results.get)
    print(f'Best model: {best_model}')
    best_model = rgsrs[best_model]
    best_model.fit(X, y)
    joblib.dump(best_model, 'model_zipcode.pkl')

if __name__ == '__main__':
    main()
