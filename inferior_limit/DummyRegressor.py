import pandas as pd
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

def main():

    dataset = pd.read_csv('../data/kc_house_data.csv')
    dataset.drop(['id', 'date', 'zipcode', 'lat', 'long'], axis=1, inplace=True)

    X = dataset.drop('price', axis=1)
    y = dataset['price']

    dummy = DummyRegressor(strategy='mean')
    dummy.fit(X, y)
    y_pred = dummy.predict(X)

    print('All data MAE:', mean_absolute_error(y, y_pred))
    print('All data MSE:', mean_squared_error(y, y_pred))

    # Splitting the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=98)

    dummy.fit(X_train, y_train)
    y_pred = dummy.predict(X_test)

    print('Test data MAE:', mean_absolute_error(y_test, y_pred))
    print('Test data MSE:', mean_squared_error(y_test, y_pred))

if __name__ == '__main__':
    main()
