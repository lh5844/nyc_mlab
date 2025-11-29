import subprocess
import pandas as pd

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

