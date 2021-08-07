#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 18:34:33 2021

@author: Rajiv Sambasivan
"""
from abc import ABC, abstractmethod


# Python program showing
# abstract base class work
 
 
class DataProcessing(ABC):
 
    @abstractmethod
    def filter(self, **kwargs):
        pass
    @abstractmethod
    def transform(self, **kwargs):
        pass
    
    @abstractmethod
    def subset(self, **kwargs):
        pass

