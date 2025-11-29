import subprocess
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# query string to get relevant data
query = """
SELECT 
    date, 
    EXTRACT(HOUR FROM a.TestTime) AS hour_of_day,
    a.MeanThroughputMbps,
    a.MinRTT
FROM `measurement-lab.ndt.unified_uploads`
WHERE
  date BETWEEN "2025-01-01" AND "2025-01-07"
  AND client.Geo.city = "New York"
  AND IsValidBest = True
  AND a.MinRTT >= 0
LIMIT 1000
"""

# cmd line args for bq query cli
cmd = [
    "bq", "query",
    "--use_legacy_sql=false",
    "--format=csv",
    "--max_rows=1000",
    query
]

# run cmd and output to csv file
csv_file = "nyc_mlab_data.csv"
with open(csv_file, "w") as f:
    subprocess.run(cmd, stdout=f, check=True)

# load csv to pandas for easy data parsing
df = pd.read_csv(csv_file)

# define features and target variable 
X = df[['hour_of_day']]
y = df['MeanThroughputMbps']

# split into training and tests
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# initialize model
model = LinearRegression()
model.fit(X_train, y_train)

# predict mean throughput mbps
y_pred = model.predict(X_test)

# measure error 
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R^2 Score: {r2:.2f}")

# plot regression for visual
plt.scatter(X, y, alpha=0.5, label='Data points')
plt.plot(X_test, y_pred, color='red', label='Regression line')
plt.xlabel('Hour of Day')
plt.ylabel('Mean Throughput (Mbps)')
plt.title('Throughput vs Hour of Day in NYC (NDT tests)')
plt.legend()
plt.savefig("throughput_vs_hour_nyc.png", dpi=300, bbox_inches='tight')