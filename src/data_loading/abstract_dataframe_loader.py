#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 18:09:23 2021

@author: Rajiv Sambasivan
"""


from abc import ABC, abstractmethod


# Python program showing
# abstract base class work
 
 
class DataFrameLoader(ABC):
 
    @abstractmethod
    def get_dataframe(self):
        pass
 

