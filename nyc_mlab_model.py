import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


csv_file = "nyc_mlab_data.csv"
# load csv to pandas for easy data parsing
df = pd.read_csv(csv_file)

# remove extreme outlier
lower = df['MeanThroughputMbps'].quantile(0.01)
upper = df['MeanThroughputMbps'].quantile(0.99)
df = df[(df['MeanThroughputMbps'] >= lower) & (df['MeanThroughputMbps'] <= upper)]
        
# define features and target variable 
X = df[['hour_of_day']]
y = df['MeanThroughputMbps']

# split into training and tests
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# initialize model
model = RandomForestRegressor(
    n_estimators=200,      # number of trees
    max_depth=10,          # max depth of trees
    min_samples_leaf=10,
    random_state=42,
)

model.fit(X_train, y_train)

# predict mean throughput mbps
y_pred = model.predict(X_test)

# measure error for ML model on raw data
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"Data points RMSE: {rmse:.2f}")
