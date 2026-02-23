# Predicting NYC Internet Throughput by Hour of Day Using Random Forest Regression

## Project Overview

Research Question:

> How does the time of day affect internet performance (mean throughput in Mbps) in New York City, and can we predict mean throughput at different hours using regression?

The goal was to identify **hourly trends** in users’ mean throughput and build a model to make informed predictions about when internet performance is likely to be better or worse in NYC.

---

## Data Source

The data comes from **Measurement Lab (M-Lab)**, an open-source internet measurement platform. To get access to M-Lab dataset: https://www.measurementlab.net/data/docs/bq/quickstart/

I queried **5,000 timestamped records** of mean throughput from New York City users.

---

## Approach

### Choosing a Model

The dataset exhibited **high variance and considerable spread**, with no strict linear relationship between the hour of day and mean throughput. Other unmeasured factors also affect throughput, making a simple linear regression unsuitable.  

Benefits of Random Forest:

- Learns **non-linear relationships** without feature scaling.
- Aggregates multiple decision trees → **robust to noise**.
- Well-suited for **real-world network performance data**.

### Data Preprocessing

1. Removed **extreme outliers**  
2. Extracted the **hour** from each timestamp to use as the model feature.  
3. Trained the **Random Forest regression** to predict mean throughput using only the hour of the day.

### Model Evaluation

The model was evaluated using **Root Mean Squared Error (RMSE)**:

1. **Point-Level RMSE:** Measures prediction error for individual data points.  
   - Result: **103.07 Mbps**  
   - High due to other unmodeled factors affecting individual throughput.  
   - Illustrated in **Figure 1**, showing predictions versus widely scattered individual points.

2. **Hourly Trend RMSE:** Measures prediction error for **hourly averages**, assessing how well the model captures overall daily trends.  
   - Result: **4.02 Mbps**  
   - Much lower, indicating accurate population-level trend predictions.  
   - Illustrated in **Figure 2**, where predicted trends closely follow actual hourly trends.  

> The second RMSE is more relevant to the problem, as the goal is **population-level trends**, not individual predictions.

---

## Results: Hourly Internet Trends

The model revealed the following patterns:

- **Lowest mean throughput:** 8 AM — likely due to increased demand as people start their day.  
- **Sustained high throughput:** 11 AM – 11 PM — suggests network infrastructure efficiently handles peak demand during working and evening hours.  
- **Spike in throughput:** 2 AM — likely due to minimal network usage and reduced contention.

**Interpretation:** Although one might expect internet performance to be worse during peak working hours, ISPs design networks to distribute capacity optimally, leading to **higher throughput during the day** than expected.

---

## Conclusion

- **Random Forest regression** effectively captures hourly trends in NYC internet throughput.  
- Individual predictions remain noisy due to unmodeled factors.
- Data sample could be parsed by time as a feature: weekday/weekend, month, year 
- Future work could include additional features to **improve prediction accuracy** and provide deeper insights into optimizing network performance.

--- 

## Figures

- **Figure 1:** Predicted throughput vs individual data points (high variance)  
- **Figure 2:** Predicted vs actual hourly average throughput (low RMSE, accurate trends)
