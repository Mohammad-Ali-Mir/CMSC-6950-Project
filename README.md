This repository is created for the CMSC-6950 project (Fall 2023) course.

In the following, you will see a full guide to understand the project and reproduce the figures.

# 1. Description of Dataset
Climate data for St. John's, sourced from https://stjohns.weatherstats.ca/download.html.
We obtained 730 (two-year) daily data points from November 01, 2021, to October 31, 2023.
## 1.1.	Attributes
<caption>Dataset Overview of Used Columns</caption>

| Feature Name                   | Description                                                            | Short Name         |
|---------------------------------|------------------------------------------------------------------------|--------------------|
| date                            | date as index (yyyy-mm-dd)                                            | date               |
| max_temperature                 | daily minimum temperature (°C)                                        | Max Temp           |
| min_temperature                 | daily minimum temperature                                              | Min Temp           |
| avg_temperature                 | average between the daily maximum and minimum temperatures            | Avg Temp           |
| avg_hourly_temperature          | average of all the hourly temperatures within the day                  | Avg hr Temp        |
| max_wind_speed                  | daily maximum wind speed (km/h)                                       | Max Wind           |
| min_wind_speed                  | daily minimum wind speed                                               | Min Wind           |
| avg_hourly_wind_speed           | average between the daily maximum and minimum wind speeds              | Avg hr Wind        |
| precipitation                   | amount of rain/snow/etc. received. 1cm snow ~ 1mm precipitation. The exact amount depends on snow density (mm) | Precip |
| avg_hourly_relative_humidity    | average of all the hourly relative humidities within the day (%)       | Avg hr Humid       |
| avg_hourly_pressure_sea         | average of all the hourly pressures within the day (kPa)               | Avg hr Press       |
| avg_hourly_visibility           | average of all the hourly visibilities within the day (m)             | Avg hr Visib       |
# 2.	Methodology
- Present (visualize) data to understand its characteristics. 
- Introduce different approaches to detect extreme values.
- Explore trends in our data.
## 2.1.	Initial Data Presentation (Visualization)
- Present our temperature group data in one time series plot.
- Do descriptive statistics of our data and show their probability distributions.
## 2.2.	Extreme Values
- Plot boxplots of the columns.
- Use Inter quartile Range (IQR) method to replace the outliers with the IQR limits:

$$
IQR = Q_3 - Q_1
$$

$$
Upper/Lower ~ limits = Q_1 ± scale ~ × ~IQR
$$

As our (temperature) data follows a cyclical pattern and experiences regular bumps based on seasonal variations, the assumption of a normal distribution may not hold. So, we focused on using a comparison with historical values.
- Use 30-year historical (normal) values for `max_temperature` and `min_temperature`.
- Pinpoint data points placed outside a threshold up and down from their corresponding historical values.
- Analyze sensitivity for values of 5 and 10 days. 
- Study descriptive statics of the extreme values: `count, mean, std, min, 25%, 50%, 75%, max`.
## 2.3.	Trends
- **Correlation Heatmap**:
  
  Survey the relationship between every two features from all columns
- **Moving Average** over features:
  
  Visualize a moving average time series with a favorite window size (10, 30 days, etc.) over an original column data 
- **Monthly Average Total Precipitation Barplot**:
  
  Sum up the total precipitation for each month and average it for all the same months as a group. Then, show results in a bar plot
# 3. Full Instruction to Reproduce Figures in Report
## 3.1.	Project Files & Folders
In this project, we performed the analyses through the `code_project.ipynb` available in the `code` folder. In that folder, We have defined some computational functions in `functions.py` and have tested them sufficiently by `pytest` in `test_functions.py`.

The used dataset is in the `data` folder. The `daily.csv` file contains daily climate data for the mentioned period, and the `normal_daily.csv` file contains the 30-year historical values.

Our produced results (plots) are in the `figures` folder.

You can access the proposal and project report files in the 'reports' folder.
## 3.2.	Prerequisites
To install the required libraries, use the following command:

```python
pip install -r requirements.txt
```

This command will install the libraries listed in the `requirements.txt` file.
## 3.3.	Run
If you open the `code_project.ipynb` file in the `code` folder and open it using `Jupyter Notebook` and click on the `Restart and Run All Cells` option, all results and figures will be produced automatically. You don't need to do any other steps. But just in case if the user want to know more, he can follow the below steps:
## 3.4.	Figure 1
