#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 18:11:57 2021

@author: Rajiv Sambasivan
"""
from abstract_dataframe_loader import DataFrameLoader
import pandas as pd

class LocalDataFrameLoader(DataFrameLoader):
    
    def get_dataframe(self):
        self.df= pd.read_excel('https://github.com/rajivsam/cmi_count_data_modeling/blob/data_branch/data/Online%20Retail.xlsx?raw=true')
        return self.df
 
