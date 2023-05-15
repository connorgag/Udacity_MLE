from sklearn.linear_model import LogisticRegression
import argparse
import os
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from azureml.core import Workspace, Dataset

def clean_data(df):
    numeric_cols = df.select_dtypes(exclude=['object']).columns
    # create a new dataframe with only the numeric columns
    df_numeric = df[numeric_cols]

    # Remove data leakage
    df_numeric = df_numeric.drop(['_RFHLTH'], axis='columns')
    df_numeric = df_numeric.fillna(0)
    y_df = df_numeric.pop('GENHLTH')
    return df_numeric, y_df


def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--max_iter', type=int, default=500, help="Maximum iterations for the solver to converge")
    parser.add_argument('--activation', type=str, default='relu', help="Activation function for the model")

    args = parser.parse_args()

    run = Run.get_context()
    


    run.log("Maximum Iterations:", np.float(args.max_iter))
    run.log("Activation Function:", (args.activation))

    df = pd.read_csv('behavioral_data.csv')

    x, y = clean_data(df)

    # TODO: Split data into train and test sets.
    X_train, X_test, y_train, y_test = train_test_split(x,y,
                                   random_state=60, 
                                   test_size=0.25, 
                                   shuffle=True)
    # Scale the input data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    # Train the model

    model = MLPRegressor(hidden_layer_sizes=(len(x.columns), 150, 50), activation=args.activation, solver='adam', max_iter=args.max_iter)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Calculate range of target variable
    y_range = np.max(y_test) - np.min(y_test)

    # Calculate NRMSE
    nrmse = rmse / y_range

    print('Mean Squared Error:', mse)
    print('R-squared:', r2)
    
    run.log("normalized_root_mean_squared_error", np.float(nrmse))

    os.makedirs('outputs', exist_ok=True)
    joblib.dump(model, 'outputs/model.joblib')

    
if __name__ == '__main__':
    main()