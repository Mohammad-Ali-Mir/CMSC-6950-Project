import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import MonthLocator, DateFormatter
import matplotlib.ticker as ticker
import calendar


def iqr_limits(data=[], scale=1.5):
    if isinstance(data, pd.Series):
        data = data.tolist()  # Convert Series to list
    if len(data) == 0:
        return None
    if not isinstance(scale, (float, int)) or scale < 0:
        scale = 1.5

    try:
        q1 = np.quantile(data, 0.25)
        q3 = np.quantile(data, 0.75)
        iqr = q3 - q1
        low_lim = q1 - scale * iqr
        high_lim = q3 + scale * iqr
        limits = [low_lim, high_lim]
        return limits
    except Exception:
        return None


def historical_extremes(data, history_data, sensitivity=10):
    if len(data) == 0 or len(history_data) == 0:
        return pd.Series(None, None, dtype='float64')
    if not isinstance(sensitivity, (float, int)) or sensitivity < 0:
        sensitivity = 10
    if sensitivity < 0:
        sensitivity = -sensitivity
    if isinstance(data, list):
        data = pd.Series(data)
    if isinstance(history_data, list):
        history_data = pd.Series(history_data)

    flags = np.where((data < history_data - sensitivity) |
                     (data > history_data + sensitivity),
                     'Extreme', 'Normal')

    extreme_indices = np.where(flags == 'Extreme')[0]
    extreme_data = data[extreme_indices]

    return extreme_data.astype('float')
################################################
def time_series_temperatures(df):
    
    # Set the style for Seaborn
    sns.set(style="whitegrid")

    # Create a time series plot for temperature
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot the temperature columns with Seaborn
    sns.lineplot(data=df, x=df.index, y='max_temperature', ax=ax, label='Max Temperature', color='red')
    sns.lineplot(data=df, x=df.index, y='avg_temperature', ax=ax, label='Avg Temperature', color='black')
    sns.lineplot(data=df, x=df.index, y='min_temperature', ax=ax, label='Min Temperature', color='blue')

    # Customize the plot
    ax.legend(loc='upper left', bbox_to_anchor=(-0.01, 1.15))
    ax.set_xlabel('\nDate\n\n(From 2021-11-01 to 2023-10-31)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Over Time')

    # Set grids
    ax.minorticks_on()
    plt.grid(True, which='major', linestyle='-', linewidth=0.8, color='gray')
    plt.grid(True, which='minor', linestyle='--', linewidth=0.5, color='gray')

    ax.set_xlim((df.index.min(), df.index.max()+pd.Timedelta(days=1)))

    month_locator = MonthLocator(interval=4)
    ax.xaxis.set_major_locator(month_locator)

    ax.xaxis.set_minor_locator(MonthLocator())

    plt.tight_layout()
    plt.savefig('../figures/1.png', facecolor='w', dpi=200)
    plt.show()


def plot_histograms_density(df, columns):
    L = len(columns)
    fig, axs = plt.subplots(L, 1, figsize=(15, L*3))
    
    for i, c in enumerate(columns):
        df[c].hist(ax=axs[i], density=True, label="normalized histogram plot") # normalizes the density
        df[c].plot.density(ax=axs[i], label="probability density plot")
        # axs[i].set(title=f"Probabilities of {c} values")
        capital = ' '.join(word.capitalize() for word in c.split('_'))
        axs[i].set_title(rf"Probabilities of $\bf{{{capital.replace(' ', '~')}}}$ Values")
        axs[i].legend(loc="upper right")

    plt.tight_layout(pad=3)
    plt.savefig('../figures/2.png', facecolor='w', dpi=200)
    plt.show()


def boxplots(df, columns):
    L = len(columns)
    fig, axs = plt.subplots(L, 1, figsize=(15, L*3))
    axs = axs.flatten()
    for i, c in enumerate(columns):
        sns.boxplot(x=c, data=df, ax=axs[i], orient='h', width=0.3)
        # df.boxplot(c, ax=axs[i], vert=False) #c = df.columns[i]: column name

        # axs[i].set_title(f'Boxplot of the "{c}" data')
        capital = ' '.join(word.capitalize() for word in c.split('_'))
        axs[i].set_title(rf"Boxplot of $\bf{{{capital.replace(' ', '~')}}}$")

        axs[i].minorticks_on()
        axs[i].grid(True, which='major', linestyle='-', linewidth=0.8, color='gray')
        axs[i].grid(True, which='minor', linestyle='--', linewidth=0.5, color='gray')

    plt.tight_layout(pad=3.0)
    plt.savefig('../figures/3.png', facecolor='w', dpi=200)
    plt.show()


# we define a function to automatically plot each attribute time series.
def time_plot(df, columns):
    L = len(columns)
    fig, axs = plt.subplots(L, 1, figsize=(15, L*5))
    axs = axs.flatten()

    for i, c in enumerate(columns):
        # df[c].plot(ax=axs[i])
        sns.lineplot(data=df, x=df.index, y=c, ax=axs[i])  #label='Max Temperature', color='red'
        # axs[i].set(title=f'Plot of the \"{c}\" data   [{c} values VS. Time]')
        capital = ' '.join(word.capitalize() for word in c.split('_'))
        axs[i].set_title(rf"Time Series Plot of $\bf{{{capital.replace(' ', '~')}}}$ [{c} values V.S. date]")
        
        # Set grids
        axs[i].minorticks_on()
        axs[i].grid(True, which='major', linestyle='-', linewidth=0.8, color='gray')
        axs[i].grid(True, which='minor', linestyle='--', linewidth=0.5, color='gray')

        axs[i].set_xlim((df.index.min(), df.index.max()+pd.Timedelta(days=1)))
        month_locator = MonthLocator(interval=4)
        axs[i].xaxis.set_major_locator(month_locator)
        axs[i].xaxis.set_minor_locator(MonthLocator())

    plt.tight_layout(pad=3.0)
    # plt.savefig('../figures/4.png', facecolor='w', dpi=600)
    plt.show()


def remove_outliers_IQR(df, columns, scale=1.5, mode="replace"):
    # outliers = pd.DataFrame()
    for c in columns:
        [low_lim, high_lim] = iqr_limits(data=df[c], scale=scale)
        # To show what percentage of each column are outliers
        Outs = df[c][(df[c] > high_lim) | (df[c] < low_lim)]
        Out_Ratio = 100*(len(Outs)/len(df[c]))
        print(f"Outliers Ratio of {c} was: %{np.round(Out_Ratio, 2)}")
        # print(f"High Limit of ({c}): {high_lim};\t Low Limit of ({c}): {low_lim}")

        ## We can replace or remove the outliers: replace/remove
        if mode == "remove":
            indexes = Outs.index
            df.loc[indexes, c] = np.nan  # put nan
        else:
            df[c] = np.where(df[c] >= high_lim, high_lim, np.where(df[c] <= low_lim, low_lim, df[c]))  # replace
        
    print("\n")
    df.info()


def plot_orig_modif_series(original, modified, columns, title='Original Plot & Modified Plot'):
    L = len(columns)
    fig, axs = plt.subplots(L, 1, figsize=(15, L*3))
    fig.suptitle(title, fontsize=16, y=0.99)
    axs = axs.flatten()
    # x_range = (original.index.min(), original.index.max())
 
    for i, c in enumerate(columns):
        # because our data is large, and is measured hourly,
        # we use every n_th row to visualize our data less densely.
        sns.lineplot(data=original[::5], x=original[::5].index, y=c, ax=axs[i], label='Original', linewidth=3, color='black', alpha=1)
        sns.lineplot(data=modified[::5], x=modified[::5].index, y=c, ax=axs[i], label='Modified', linewidth=3, color='red', alpha=0.6)

        axs[i].legend(loc='upper right')
        # axs[i].set(title=f'{c} values VS. Time')
        capital = ' '.join(word.capitalize() for word in c.split('_'))
        axs[i].set_title(rf"$\bf{{{capital.replace(' ', '~')}}}$ Values VS. Time")

        # Set grids
        axs[i].minorticks_on()
        axs[i].grid(True, which='major', linestyle='-', linewidth=0.8, color='gray')
        axs[i].grid(True, which='minor', linestyle='--', linewidth=0.5, color='gray')
        axs[i].set_xlim((original.index.min(), original.index.max()+pd.Timedelta(days=1)))
        month_locator = MonthLocator(interval=4)
        axs[i].xaxis.set_major_locator(month_locator)
        axs[i].xaxis.set_minor_locator(MonthLocator())
        
    plt.tight_layout(pad=3)
    plt.savefig('../figures/4.png', facecolor='w', dpi=200)
    plt.show()


def historical_temperatures(df_c, df_hist, sens=[5, 10]):

    # Set the style for Seaborn
    sns.set(style="whitegrid")
    # Create a time series plot for temperature
    fig, ax = plt.subplots(len(sens), 1, figsize=(12, 15))
    axs = ax.flatten()
    c1 = 'max_temperature'; c1_historical = 'max_temperature_v'
    c2 = 'min_temperature'; c2_historical = 'min_temperature_v'

    for i, s in enumerate(sens):
        # Plot the temperature columns with Seaborn
        sns.lineplot(data=df_c, x=df_c.index, y=c1, ax=axs[i], label='Max Temperature', color='red')
        sns.lineplot(data=df_hist, x=df_hist.index, y='max_temperature_v', ax=axs[i], label='Historical Max Temperature', color='black')

        sns.lineplot(data=df_c, x=df_c.index, y=c2, ax=axs[i], label='Min Temperature', color='blue')
        sns.lineplot(data=df_hist, x=df_hist.index, y='min_temperature_v', ax=axs[i], label='Historical Min Temperature', color='black')

        data_extreme = historical_extremes(df_c[c1], df_hist[c1_historical], sensitivity=s)
        label = rf"Extremes (More than $\bf{str(s)}$ days)"
        axs[i].scatter(data_extreme.index, data_extreme, label=label, color='yellow', marker='o', s=50, edgecolors= "black")
        print(f"**Extremes for Max Temperature (More than \"{s}\" days)**\n{data_extreme.describe()}\n\n")

        data_extreme = historical_extremes(df_c[c2], df_hist[c2_historical], sensitivity=s)
        label = rf"Extremes (More than $\bf{str(s)}$ days)"
        axs[i].scatter(data_extreme.index, data_extreme, label=label, color='cyan', marker='o', s=50, edgecolors= "black")
        print(f"**Extremes for Min Temperature (More than \"{s}\" days)**\n{data_extreme.describe()}\n\n")

        # Customize the plot
        axs[i].set_xlabel('Date\n\n(From 2021-11-01 to 2023-10-31)')
        axs[i].set_ylabel('Temperature (°C)')
        axs[i].set_title('Max/Min Temperatures Over Time')

        # Set grids
        axs[i].minorticks_on()
        axs[i].grid(True, which='major', linestyle='-', linewidth=0.8, color='gray')
        axs[i].grid(True, which='minor', linestyle='--', linewidth=0.5, color='gray')

        axs[i].set_xlim((df_c.index.min(), df_c.index.max()+pd.Timedelta(days=1)))

        month_locator = MonthLocator(interval=4)
        axs[i].xaxis.set_major_locator(month_locator)
        axs[i].xaxis.set_minor_locator(MonthLocator())

        # Move the legend outside the plot
        axs[i].legend(loc='upper left', bbox_to_anchor=(0, 1.5))

    plt.tight_layout()
    plt.savefig('../figures/5.png', facecolor='w', dpi=200)
    plt.show()


def heatmap(df, column_mapping=None):
    if column_mapping is None:
        column_mapping = df.columns

    cor_matrix = df.corr()  # df.loc[:,:"precipitation"].corr()
    cor_matrix = cor_matrix.rename(columns=column_mapping, index=column_mapping)

    # Create a mask to hide the upper triangle
    mask = np.triu(np.ones_like(cor_matrix), k=1)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cor_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f", mask=mask) # xticklabels=df.index.date, yticklabels=df.index.date

    plt.xticks(rotation=45, ha='right')
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('../figures/6.png', facecolor='w', dpi=200)
    plt.show()


def plot_moving_average(df, columns, window_size=30):
    df_c = df.copy()
    L = len(columns)
    fig, axs = plt.subplots(L, 1, figsize=(15, L*5))
    axs = axs.flatten()
    x_range = (df.index.min(), df.index.max())
    
    for i, c in enumerate(columns):
        # Calculate the moving average
        df_c['moving_average'] = df_c[c].rolling(window=window_size, center=True).mean()

        # Plot original data & moving average
        axs[i].plot(df_c.index, df_c[c], label='Original Data', color='gray')
        axs[i].plot(df_c.index, df_c['moving_average'], label=f'Moving Average (Window={window_size} days)', color='blue')

        capital = ' '.join(word.capitalize() for word in c.split('_'))
        axs[i].set_title(rf"$\bf{{{capital.replace(' ', '~')}}}$ Over Time with Moving Average")
        axs[i].set_xlabel('Date')
        axs[i].set_ylabel(f'{c}')
        axs[i].legend()
        axs[i].set_xlim(x_range)
        axs[i].grid(True)
    
    plt.tight_layout()
    plt.savefig('../figures/7.png', facecolor='w', dpi=200)
    plt.show()


def precipitation_monthly(df_c):
    # Assuming df is your DataFrame with a datetime index and a 'precipitation' column
    df_c['year'] = df_c.index.year
    df_c['month'] = df_c.index.month

    # Group by year and month, summing precipitation values
    monthly_precipitation_sums = df_c.groupby(['year', 'month'])['precipitation'].sum().reset_index()

    # Calculate the average precipitation for each month across different years
    average_precipitation_by_month = monthly_precipitation_sums.groupby('month')['precipitation'].mean().reset_index()

    # Set the style for Seaborn
    sns.set(style="whitegrid")

    # Create a bar plot for average precipitation by month
    # plt.figure(figsize=(10, 6))
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='month', y='precipitation', data=average_precipitation_by_month, color='blue')

    # Customize the plot
    plt.xlabel('Month')
    plt.ylabel('Average Precipitation')
    plt.title('Average Monthly Precipitation Across Years')
    plt.xticks(range(0, 12), calendar.month_name[1:], rotation=45)  # month names on x-axis

    # # horizontal gridlines
    ax.set_yticks((0, 251), minor=True)

    # Add minor y-ticks
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    # Add grids
    ax.yaxis.grid(True, which='both', color='0.8')

    plt.tight_layout()
    plt.savefig('../figures/8.png', facecolor='w', dpi=200)
    plt.show()


def pairplot(df, column_mapping=None):
    if column_mapping is None:
        column_mapping = df.columns

    df_pair = df.copy()  # df.loc[:,:"precipitation"]
    df_pair = df_pair.rename(columns=column_mapping)

    sns.pairplot(df_pair[df_pair.columns], corner=True, diag_kind=None)

    plt.tight_layout()
    plt.savefig('../figures/10.png', facecolor='w', dpi=500)
    plt.show()
