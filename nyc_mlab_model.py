import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
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
    min_samples_leaf=5,
    random_state=42,
)

model.fit(X_train, y_train)

# predict mean throughput mbps
y_pred = model.predict(X_test)

# measure error for ML model on raw data
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"Data points RMSE: {rmse:.2f}")

# compute MeanThroughput averages for each hour to see hourly trends for actual and pred
actual_hourly_avg = df.groupby('hour_of_day')['MeanThroughputMbps'].mean().reset_index()
pred_df = pd.DataFrame({'hour_of_day': X_test['hour_of_day'], 'y_pred': y_pred})
pred_hourly_avg = pred_df.groupby('hour_of_day')['y_pred'].mean().reset_index()

# RMSE for hourly average trends
hourly_rmse = np.sqrt(mean_squared_error(actual_hourly_avg['MeanThroughputMbps'], 
                                         pred_hourly_avg['y_pred'].reindex(actual_hourly_avg.index, fill_value=0)))
print(f"Hourly average RMSE: {hourly_rmse:.2f}")

# Plot 1: show raw data and predicted hourly trend to demonstrate raw data RMSE
plt.figure(figsize=(12,7))
plt.scatter(df['hour_of_day'], df['MeanThroughputMbps'], alpha=0.3, label='Raw Data')
plt.plot(pred_hourly_avg['hour_of_day'], pred_hourly_avg['y_pred'], color='red', linestyle='--', marker='x', label='Predicted Hourly Avg')
plt.xlabel('Hour of Day')
plt.ylabel('Mean Throughput (Mbps)')
plt.title('NYC Internet Throughput vs Hour of Day (Raw Data + Predicted Trend)')
plt.xticks(range(0,24))
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("nyc_throughput_raw_vs_predicted_trend.png", dpi=300, bbox_inches='tight')

# Plot 2: show actual and predicted hourly avg trends
plt.figure(figsize=(12,7))
plt.plot(actual_hourly_avg['hour_of_day'], actual_hourly_avg['MeanThroughputMbps'], color='blue', marker='o', label='Actual Hourly Avg')
plt.plot(pred_hourly_avg['hour_of_day'], pred_hourly_avg['y_pred'], color='red', linestyle='--', marker='x', label='Predicted Hourly Avg')
plt.xlabel('Hour of Day')
plt.ylabel('Mean Throughput (Mbps)')
plt.title('NYC Internet Throughput vs Hour of Day (Trend Only)')
plt.xticks(range(0,24))
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("nyc_throughput_trends.png", dpi=300, bbox_inches='tight')