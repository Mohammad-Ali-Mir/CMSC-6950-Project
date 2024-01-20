This repository is created for the CMSC-6950 project (Fall 2023) course.

In the following, you will see a full guide to understand the project and reproduce the figures.

# 1. Description of Dataset
Climate data for St. John's, sourced from https://stjohns.weatherstats.ca/download.html.
We obtained 730 (two-year) daily data points from November 01, 2021, to October 31, 2023.
## 1.1. Attributes
<caption>Dataset Overview of Used Columns</caption>

| Feature Name                   | Description                                                           | Short Name         |
|---------------------------------|-----------------------------------------------------------------------|--------------------|
| date                            | date as index (yyyy-mm-dd)                                           | date               |
| max_temperature                 | daily minimum temperature (°C)                                       | Max Temp           |
| min_temperature                 | daily minimum temperature                                             | Min Temp           |
| avg_temperature                 | average between the daily maximum and minimum temperatures           | Avg Temp           |
| avg_hourly_temperature          | average of all the hourly temperatures within the day                 | Avg hr Temp        |
| max_wind_speed                  | daily maximum wind speed (km/h)                                      | Max Wind           |
| min_wind_speed                  | daily minimum wind speed                                              | Min Wind           |
| avg_hourly_wind_speed           | average between the daily maximum and minimum wind speeds             | Avg hr Wind        |
| precipitation                   | amount of rain/snow/etc. received. 1cm snow ~ 1mm precipitation. <br> The exact amount depends on snow density (mm)| Precip |
| avg_hourly_relative_humidity    | average of all the hourly relative humidities within the day (%)      | Avg hr Humid       |
| avg_hourly_pressure_sea         | average of all the hourly pressures within the day (kPa)              | Avg hr Press       |
| avg_hourly_visibility           | average of all the hourly visibilities within the day (m)            | Avg hr Visib       |
# 2. Methodology
- Present (visualize) data to understand its characteristics. 
- Introduce different approaches to detect extreme values.
- Explore trends in our data.
## 2.1.	Initial Data Presentation (Visualization)
- Present our temperature group data in one time series plot.
- Do descriptive statistics of our data and show their probability distributions.
## 2.2.	Extreme Values
- Plot boxplots of the columns.
- Use Inter Quartile Range (IQR) method to replace the outliers with the IQR limits:

$$IQR = Q_3 - Q_1$$

$$Upper/Lower ~ limits = Q_{3/1} ± scale ~ × ~IQR$$

As our (temperature) data follows a cyclical pattern and experiences regular bumps based on seasonal variations, the assumption of a normal distribution may not hold. So, we focused on using a comparison with historical values.
- Use 30-year historical (normal) values for `max_temperature` and `min_temperature`.
- Pinpoint data points placed outside a threshold up and down from their corresponding historical values.
- Analyze sensitivity for values of 5 and 10 days. 
- Study descriptive statics of the extreme values: `count, mean, std, min, 25%, 50%, 75%, max`.
## 2.3.	Trends
- **Correlation Heatmap**:
  
  Survey the relationship between every two features from all columns
- **Moving Average**:
  
  Visualize a moving average time series with a favorite window size (10, 30 days, etc.) over an original column data 
- **Monthly Average Total Precipitation Barplot**:
  
  Sum up the total precipitation for each month and average it for all the same months as a group. Then, show results in a bar plot
# 3. Figures Reproduction 
## 3.1.	Project Files & Folders
- In this project, we performed all analyses through the `code_project.ipynb` available in the `code` folder. In that folder, We have defined all the functions in `functions.py` and have tested the computational ones (the first two) sufficiently by `pytest` in `test_functions.py`.
- The used dataset is in the `data` folder. The `daily.csv` file contains daily climate data for the mentioned period, and the `normal_daily.csv` file contains the 30-year historical values.
- Our produced results (plots) are in the `figures` folder.
- You can access the proposal and project report files in the `reports` folder.
## 3.2.	Prerequisites
The `requirements.txt` file has mentioned the appropriate library names and their versions used in our project.
## 3.3.	Run
You can simply open the `code_project.ipynb` file in the `code` folder, use `Jupyter Notebook`, click on the `Restart and Run All Cells` option, then, all results and figures will be produced automatically. You don't need to do any other steps. But just in case the user wants to know more about the specifics of production of each figure, they can follow the below steps:
## 3.4. Full Instruction to Reproduce Figures in Report
First, you need to do the initial set ups and imports in the `code` folder:

```
from functions import *

# Load data
cols = ['date','max_temperature','min_temperature','avg_hourly_temperature','avg_temperature',\
        'max_wind_speed','avg_hourly_wind_speed','min_wind_speed','precipitation',\
        'avg_hourly_relative_humidity','avg_hourly_pressure_sea','avg_hourly_visibility']
df = pd.read_csv('../data/daily.csv', parse_dates=['date'], index_col=['date'], dayfirst=True, usecols=cols)

hist_cols = ['date','max_temperature_v','min_temperature_v','max_wind_speed_v','min_wind_speed_v','precipitation_v']
df_hist = pd.read_csv('../data/normal_daily.csv', parse_dates=['date'], index_col=['date'], dayfirst=True, usecols=hist_cols)

selected_cols = ['avg_hourly_temperature','avg_hourly_wind_speed','precipitation']
column_mapping = {
      'max_temperature': 'Max Temp',
      'min_temperature': 'Min Temp',
      'avg_hourly_temperature': 'Avg hr Temp',
      'avg_temperature': 'Avg Temp',
      'max_wind_speed': 'Max Wind',
      'avg_hourly_wind_speed': 'Avg hr Wind',
      'min_wind_speed': 'Min Wind',
      'avg_hourly_relative_humidity': 'Avg hr Humid',
      'avg_hourly_pressure_sea': 'Avg hr Press',
      'avg_hourly_visibility': 'Avg hr Visib',
      'precipitation': 'Precip'}
```

___
### 3.4.1. Figure 1: Time-series illustration
<details><summary>What this figure does:</summary>  
In this figure, we aim to get to know our data (temperature group) by plotting them in the same time-series plot.

<p>&nbsp;</p>

In Figure 1, We have plotted `max_temperature`, `min_temperature`, `avg_temperature` as red, blue, and black lines, respectively, over `date` in one time-series plot. As you can see, the average temperature has been placed between the maximum and minimum temperatures. You can see the time series over the two years (2021-11-01 to 2023-10-31). We can also have the time series plots for the other features, but we showed temperatures as samples.
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/a87addf7-efea-4806-bda7-148a3728dc25)
</details> 

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
df_copy = df.copy()
time_series_temperatures(df_copy)
```
___
### 3.4.2. Figure 2: Probability density and normalized histogram distributions
<details><summary>What this figure does:</summary>  
The histograms were plotted using `plot_histograms_density` function. In that function, we used `.hist` and `.density` to plot the distribution of our columns' probabilities.

<p>&nbsp;</p>

The plot is shown for `avg_hourly_temperature`, `avg_hourly_wind_speed`, and `precipitation` features. 
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/a9fdd7a6-106e-42a6-8dad-9d6e83275293)
</details>

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
plot_histograms_density(df, selected_cols)
```
___
### 3.4.3. Figure 3: Boxplots for selected columns
<details><summary>What this figure does:</summary>  
We want to see the boxplots of our columns. In this way, we can clearly understand the distribution and outliers of our data.

<p>&nbsp;</p>

Boxplots were plotted for selected columns: `avg_hourly_temperature`, `avg_hourly_wind_speed`, and `precipitation`. The points outside the 1.5 x interquartile range are outliers. Outliers based on IQR method are enormous for precipitation. For `avg_hourly_temperature`, we do not see any outliers.
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/42dc4963-b351-4188-b8fa-ec19d593149e)
</details> 

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
boxplots(df, selected_cols)
```
___
### 3.4.4. Figure 4: Illustration of modified & original columns time series
<details><summary>What this figure does:</summary>  
The used scale in (scale x IQR) is 1.5. Orange shows parts of the original time series replaced by upper or lower IQR method limits. We see a massive correction for precipitation. Outlier ratios are 0, 1.23, and 12.19% of the data points in the above features, respectively.

<p>&nbsp;</p>

To remove outliers, we developed `remove_outliers_IQR` function. In this function, the computational `iqr_limits` function is used for calculating the IQR limits (its test function is available in `test_functions.py` as `test_iqr_limits`). Use `plot_orig_modif_series` function to plot both versions of the original and modified time series on one plot.
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/3d2b619f-02cf-4f08-97aa-755f3bc7f29a)
</details>

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
df_iqr = df.copy()[selected_cols]       
remove_outliers_IQR(df_iqr, df_iqr.columns, scale=1.5)
plot_orig_modif_series(original=df.copy()[selected_cols], modified=df_iqr, columns=df_iqr.columns, title=f"Original Plot & Modified Plot\n\
(Outliers Replaced by IQR Limits, Scale = 1.5)")
```
___
### 3.4.5. Figure 5: Illustration of extreme values detection using historical values
<details><summary>What this figure does:</summary>  
Extreme values (yellow and cyan color points) are detected respectively for `max_temperature` and `min_temperature` values (red and blue time series). Historical time series for both high and low temperatures are the two comparatively parallel black lines. The sensitivity values tested for threshold are 5 and 10 days above/below a historical line for each of the temperature lines separately. We see extreme values mostly around pits and peaks in historical trend lines.

<p>&nbsp;</p>

We illustrated specifically for `max_temperature` and `min_temperature`. In this approach, we developed a computational function called `historical_extremes` (its test function available in `test_functions.py` as `test_historical_extremes`) to pinpoint those data points (plotted as a scatter plot) placed outside of a threshold up and down from their corresponding historical values. We analyzed its sensitivity for values of 5 and 10 and have compared the plots. 
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/5924b8ed-3422-47a2-9f4b-55706bddb2f6)
</details> 

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
df_c = df.copy()
sens = [5, 10]  # sensitivities
historical_temperatures(df_c, df_hist, sens=[5,10])
```
___
### 3.4.6. Figure 6: Correlation heatmap
<details><summary>What this figure does:</summary>  
This shows the relationship between every two features from all columns. The repetitive upper triangle part of the map has been removed (by applying a mask in plotting). The red color (corresponding to +1) in the plot shows a perfect positive relationship, while blue (corresponding to -1) shows a perfect negative relationship (`coolwarm` was used for `cmap` parameter). Short names have been used for feature names using `column_mapping`.

<p>&nbsp;</p>

We used `.corr()` on our data frame to get correlation matrix; then used `sns.heatmap` to visualize the map.
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/14b63e18-44d1-4b5d-80d8-3ad9ad9f5ff0)
</details> 

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
df_c = df.copy()
heatmap(df=df_c, column_mapping=column_mapping)
```
___
### 3.4.7. Figure 7: Moving average illustration for trend extraction
<details><summary>What this figure does:</summary>  
Moving average (blue series) has been done with a window of 10 days on selected features' original data (gray series). The time span is from 2021-11-01 to 2023-10-31.

<p>&nbsp;</p>

In the Moving Average method, we have a function called `plot_moving_average`, through which you can visualize a moving average time series over the original column data with a favorite window size (10, 30 days, etc.). We used `df.rolling()` with a 10-day window size and then `.mean()` to calculate the moving averages.
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/b5af95b2-312f-4fab-9b3e-e7eb6e81dbb6)
</details> 

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
cols = selected_cols
plot_moving_average(df.copy(), columns=cols, window_size=10)
```
___
### 3.4.8. Figure 8: Average monthly precipitation bar plot
<details><summary>What this figure does:</summary>  
Each bar for each specific month shows the average of total of daily precipitations (rain, snow equivalent, etc) during that month. The precipitation unit is mm.

<p>&nbsp;</p>

What the function does is that it sums up the total precipitation in each month. Then it averages for all the same months as a group. Then, it shows the results in a bar plot.
![image](https://github.com/Mohammad-Ali-Mir/CMSC-6950-Project/assets/81976863/290448d7-79bf-4f70-94e2-1c7c00943895)
</details> 

<p>&nbsp;</p>
To reproduce this figure, just run the following after the initial imports:

```
df_c = df.copy()
precipitation_monthly(df_c)
```
