# Overview
- Describe the goal of the project
- Why is it important to extract patterns from this data. Manifold hypothesis and its relevance in machine learning. Relevance from a practical standpoint
- How are you going to extract patterns (to be done later)


# Data Description
- This is a transnational data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.
    ## Attribute Information:
    1. InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.

    2. StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.

    3. Description: Product (item) name. Nominal.

    4. Quantity: The quantities of each product (item) per transaction. Numeric.

    5. InvoiceDate: Invice Date and time. Numeric, the day and time when each transaction was generated.

    6. UnitPrice: Unit price. Numeric, Product price per unit in sterling.

    7. CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.

    8. Country: Country name. Nominal, the name of the country where each customer resides.

- There are few issues in the data set:
    1. There are total 541909 number of instances in this data set. Among these, 9288 are cancelled transactions.
    2. This data set included transactions of both registered and unregistered customers. There 135080 number of transactions made by unregistered customers.
    3. Data foe certain days are missing in this data set. For example, data for saturday is missing; we have categorized this missing data as Missing Not At Random or MNAR. Data for few other days are also missing; we have categorised this missing data as Missing at Random or MAR.

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

  We plotted bar plot having hour intervals in the x-axis and total number of customers over the whole data set in the y-axis. The frequency distribution is almost symmetric. Most of the values (over 99.9%) are between 6 AM and 9 PM. Maximum arrival is in the hour from 12 PM to 1 PM.

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
