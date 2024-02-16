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

PATH_TO_DATABASE = '../data/kc_house_data.db'

class CustomFeatureSelector:

    def __init__(self, estimator, number_logs = 6, threshold=0.2):
        self.estimator = estimator

    def fit(self, X, y):
        self.estimator.fit(X, y)
        self.feature_importances_ = self.estimator.feature_importances_
        return self

    def transform(self, X):
        for i in range(0, self.number_logs * 2, 2):
            if(self.feature_importances_[i] > self.feature_importances_[i+1]):
                X = np.delete(X, i+1, axis=1)
                self.feature_importances_.pop(i+1)
            else:
                X[:, i+1] = normalize(X[:, i+1])
                X = np.delete(X, i, axis=1)
                self.feature_importances_.pop(i)
        return X[:, self.feature_importances_ > self.threshold]

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)

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


def rearrange_columns(columnA, columnB, arr):

    # Get the index of the columns
    indexA = np.where(arr == columnA)[0][0]
    indexB = np.where(arr == columnB)[0][0]

    arr = np.concatenate((np.asarray([arr[indexA]]), arr[:indexA], arr[indexA+1:]), axis=0)
    arr = np.concatenate((np.asarray([arr[indexB]]), arr[:indexB], arr[indexB+1:]), axis=0)
    return arr



def main():

    # Load the data
    data = read_from_db()

    # Create the feature matrix and the target vector
    X = data.drop(['price', 'zipcode', 'yr_renovated', 'lat', 'long', 'sales_date', 'id'], axis=1).fillna(0)
    y = data['price']

    columns = X.columns.values
    columns = np.concatenate((columns[1:], [columns[0]]), axis = 0) ##Putting season at the end so that is never empty when we split the data

    ## Logarithm of the variables and variables in pair, first
    columns = np.delete(columns, np.where(columns == "yr_built")[0][0])
    columns = np.delete(columns, np.where(columns == "better_view")[0][0])
    columns = rearrange_columns('sqft_living', 'log_living', columns)
    columns = rearrange_columns('sqft_lot15', 'log_lot15', columns)
    columns = rearrange_columns('sqft_above', 'log_above', columns)
    columns = rearrange_columns('sqft_basement', 'log_basement', columns)
    columns = rearrange_columns('sqft_living15', 'log_living15', columns)
    columns = rearrange_columns('sqft_lot', 'log_lot', columns)

    # Define which columns to encode and which to keep as is
    columns_to_encode = ['yr_built', 'better_view']
    # Create the transformers for encoding
    ordinal_encoder = OrdinalEncoder(categories='auto')
    label_encoder = LabelEncoder()


    # Create the ColumnTransformer
    column_transformer = ColumnTransformer([
        ('ordinal', ordinal_encoder, columns_to_encode)
        ])
    X_transformed = column_transformer.fit_transform(X)
    X_not_transformed = X[columns].values
    X_not_transformed[:, -1] = label_encoder.fit_transform(X_transformed[:, -1])
    X_hole = np.concatenate((X_not_transformed, X_transformed), axis=1)

    # Create the training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_hole, y, test_size=0.2, random_state=98)
    

    forest = RandomForestRegressor(n_estimators=100)

    regressors = [
        linear_model.LinearRegression(),
        linear_model.SGDRegressor(),
        svm.LinearSVR(),
        svm.SVR(),
        RandomForestRegressor(),
    ]

    regressors = {
        'Linear': linear_model.LinearRegression(),
        'SGD': linear_model.SGDRegressor(),
        'LinearSVR': svm.LinearSVR(),
        'SVR': svm.SVR(),
        'RandomForest': RandomForestRegressor(),
    }

    params = {
        'Linear': {'fit_intercept': [True, False]},
        'SGD': {'loss': ['squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'], 'penalty': ['l2', 'l1', 'elasticnet']},
        'LinearSVR': {'C': [0.1, 1, 10], 'epsilon': [0.1, 0.2, 0.3]},
        'SVR': {'C': [0.1, 1, 10], 'epsilon': [0.1, 0.2, 0.3]},
        'RandomForest': {'n_estimators': [10, 100, 1000], 'max_features': ['auto', 'sqrt', 'log2']}
    }
    
    # Create the pipeline
    pipeline = Pipeline([
        ('feature_selection', CustomFeatureSelector(forest)),
    ])

    rgsrs = {}
    results = {}

    for model in regressors.keys():
        gs = GridSearchCV(regressors[model], params[model], cv=5)
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
    best_model.fit(X_hole, y)
    joblib.dump(best_model, 'model.pkl')