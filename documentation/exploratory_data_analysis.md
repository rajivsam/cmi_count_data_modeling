# Overview
- Describe the goal of the project
- Why is it important to extract patterns from this data. Manifold hypothesis and its relevance in machine learning. Relevance from a practical standpoint
- How are you going to extract patterns (to be done later)


# Data Description
- Short description of the business context and features in the raw data
- Summary of the issues in the data
- ## Data Cleaning:
    1. Since unsuccessful transactions does not effect the business of the store, we ignored the canceled transactions. To do so, we dropped those rows of the dataframe that had values starting with 'C' under "InvoiceNo" column.
    2. The unregistered customers do not have any customer IDs. Hence, the column "CustomerID" has null values corresponding to these unregistered customers. We dropped all those rows of the dataframe that has null values under the "CustomerID" column.

  ## Pre-processing:
  1. We converted the original dataframe into a new dataframe with columns being the 24 one hour intervals of a day and index being the business days for which data was available. The name of the columns are 00:00:00, 01:00:00, 02:00:00,...,23:00:00.
  2. The proportion of customers between 6 a.m. to 8 p.m. is 99.9%. So we focused our analysis on the data from 6 a.m. to 8 p.m. and dropped the columns 00:00:00, 01:00:00,.., 05:00:00, 20:00:00,..., 23:00:00.
  3. We created dataframes for each quarter according to the week numbers. These dataframes are used for analysis purposes later on.
  4. For longest sequence of continuously available data of each quarter, we created a time series.  We plotted PACF plot for each time series to find lags for each quarter.
  5. For each quarter we created new dtaframe with columns being being arrivals of previous hour intervals on which arrivals of a specific hour interval is dependent, arrivals, day, week, month of that specific hour interval and index being the hour intervals for which data for the columns are available. These previous hours are calculated using lags obtained from the PACF plot for each quarter.
- Finally we have four dataframes, one for each quarter, in our hand. We had the following observations from these dataframes:
    1. We have highest number of lags i.e., more dependencies on previous hours, for the 1st quarter and least number of lags i.e., less dependencies on previous hours for 2nd quarter.
    2. The columns of each dataframe except "arr(h)" are the variables on which arr(h) (arrival of a hour interval h) is dependent on.
    3. The rows of each dataframe are mutually independent.

# Characteristics of Hourly Arrivals
- ## Hourly plots (bar plots)
  ![Bar plot](https://github.com/rajivsam/cmi_count_data_modeling/blob/documentation_branch/documentation/images/barplot.png?raw=true)


- ## Sample daily plots
  ![Sample daily plots](https://github.com/rajivsam/cmi_count_data_modeling/blob/documentation_branch/documentation/images/sample_plot.png?raw=true)

  We plotted sample daily bar plots by sampling three days of data from each quarter. These sample plots reflects the original distributions of each quarter. From these plots we can say the frequency distribution of the data of first three quarters are positively skewed whereas the frequency distribution of the data of 4th quarter is symmetric.
- ## Moving average plot of hourly arrivals with daily window
  ![Moving average daily plots](https://github.com/rajivsam/cmi_count_data_modeling/blob/documentation_branch/documentation/images/MA_daily_plot.png?raw=true)

  We plotted moving average with daily window for each quarter by taking a window of 14 observations (6 a.m. to 8 p.m.). We observed certain fluctuations in the plot over the data of each quarter. On further inspection we concluded these are weekly fluctuations meaning the data varies significantly over the 6 days (Sunday to Friday) of each week.
- ## MA mean plot
- ## MA variance plot
- Short discussion of the above characteristics


# Summary of Salient Facts from EDA
- To do
