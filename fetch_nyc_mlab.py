import subprocess
import pandas as pd
import numpy as np


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
LIMIT 5000
"""

# cmd line args for bq query cli
cmd = [
    "bq", "query",
    "--use_legacy_sql=false",
    "--format=csv",
    "--max_rows=5000",
    query
]

# run cmd and output to csv file
csv_file = "nyc_mlab_data.csv"
with open(csv_file, "w") as f:
    subprocess.run(cmd, stdout=f, check=True)

print("nyc_mlab_data.csv has been created")