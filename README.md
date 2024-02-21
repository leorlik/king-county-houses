# King County House Price Predictions

Prediction of house prices in the House Sales dataset in King County, USA.

## Project Structure

- `data`: Directory containing the dataset and the created SQLite database file.
- `data_analysis`: Directory containing a notebook with the data analysis and images.
- `Docs`: Directory containing relevant documents and links about the project.
- `Environment`: Directory containing files about the virtual environment used for this project.
- `inferior_limit`: Directory containing a script with a Dummy Regressor to set a limit on model performance.
- `Models`: Directory containing scripts and saved models.
- `Scripts`: Directory containing various scripts, including those for SQL saving and variable book.

## About the Project

In this repository, the [King County sales dataset](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction) is explored to predict house sale prices. The data was analyzed in a [Jupyter notebook](https://github.com/leorlik/king-county-houses/blob/main/data_analysis/Data%20Analysis%20House%20Prices.ipynb), stored in SQLite3, and variables were created. Scikit-learn was used to predict prices in multiple contexts, with the best model being saved after a GridSearch. The best model achieved an R2 Score of 0.839, using a Random Forest with 1000 estimators, standard scaler, and zipcode as dummies (in zipcode\_model script).

