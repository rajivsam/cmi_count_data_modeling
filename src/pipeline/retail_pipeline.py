#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pipeline for EDA https://github.com/rajivsam/cmi_count_data_modeling/blob/common_code_16_08_2021/notebooks/arrivals_EDA.ipynb

This script creates the required hourly arrival datasets for all 4 quarter in the year 2011.

Dependencies
------------
Files and Folders: This python file 'retail_pipeline.py' is in current working directory and two directories 'data_loading', 'data_processing' should be in the parent directory.
'data_loading' contains 'local_dataframe_loader.py' and 'abstract_dataframe_loader.py'
'data_processing' contains 'retail_data_processing.py' and 'abstract_data_processing.py'

Outputs
-----------
On a succesful execution, 4 csv files will be saved in in ../data directory. Each file is related to the longest sequence of available data in respective quarter.
Each row corrosponds to an hour of a particular day. For a sequence of significant lags [l1,l2,...,ln] each row represents <h,arr(h-l1),arr(h-l2),...,arr(h-ln),Week,Day,Month,arr(h)>.
h: Hour
arr(h): Number of customer arrival in the hour between h:00:00 and (h+1):00:00
Week: Week number
Day: Day of the week
Month: Month number
"""
# Importing the modules
import sys
sys.path.append('../data_loading')
from local_dataframe_loader import *
sys.path.append('../data_processing')
from retail_data_processing import *

# Instantiating a LocalDataFrame loader
x = LocalDataFrameLoader()

# Loading the dataframe
data = x.get_dataframe()

# Instantiating a RetailDataProcessing object
y = RetailDataProcessing()

# (a) Invoke the filter method to apply business rules
filtered_data = y.filter(x.df)

# (b) Invoke the transform method to get daily hourly counts
transformed_data = y.transform(filtered_data)

# Drop the less important columns
dropped_data = y.drop_columns(transformed_data)

# (c) Subset dataframe to quarters
subset_data = y.subset(dropped_data)

# (d)Invoke the tansform pacf_sequence to get the pandas time series for different quarters
Q_ts = {}
for i in range(1, 5):
    Q_ts[i] = y.transform_pacf_sequence(subset_data['Q'+str(i)])


lag = {}
lag['Q1'] = [28, 26, 25, 21, 20, 19, 18, 17,
             14, 13, 12, 11, 10, 9, 7, 6, 5, 4, 3, 2, 1]
lag['Q2'] = [20, 15, 14, 13, 12, 11, 10, 7, 6, 5, 4, 3, 1]
lag['Q3'] = [28, 26, 22, 20, 18, 14, 13, 12, 11, 7, 6, 5, 4, 3, 2, 1]
lag['Q4'] = [28, 25, 24, 20, 19, 18, 14, 13, 12, 11, 10, 9, 6, 5, 4, 3, 1]

#	(e) Invoke the transform_hourly_arrivals_dataset to generate the datasets for the different quarters, save the dataset to the data directory.
df = {}
for i in range(1, 5):
    df['Q'+str(i)] = y.transform_hourly_arrivals_dataset(Q_ts[i],
                                                         lag=lag['Q'+str(i)])


# Write all the dataframes as csv files
for i in range(1, 5):
    df['Q'+str(i)].to_csv('../../data/Q'+str(i) +
                          '_transform_hourly_arrivals_dataset.csv')

