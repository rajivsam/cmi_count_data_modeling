#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 18:38:15 2021

@author: Rajiv Sambasivan
"""

from abstract_data_processing import DataProcessing
import pandas as pd
from numpy import nan
import itertools
import datetime

class RetailDataProcessing(DataProcessing):
    """ Performs all the preprocessing tasks required for the project on the original dataframe."""

    def filter(self, data,inplace=False,**kwargs):
        """ Filters out the data corresponding to unregistered customer ID's and cancelled transactions from the dataframe.

        Input of this method is the original dataframe. This method removes the rows in the dataframe containing null values under 'CustomerID' column and values starting with 'C' under 'InvoiceNo' column. If inplace is False then the method returns a copy of the updated dataframe; otherwise updates the input dataframe in place and returns nothing. Default is inplace = False.
        """

        if not inplace:
          data=data.copy()
        data=data.dropna(subset=['CustomerID'])
        data.drop(index=data.loc[data['InvoiceNo'].str.match(r'^C.*')==True].index,inplace=True)
        return data

    def transform(self,data,inplace=False, **kwargs):
        """ Transforms the filtered dataframe into a new dataframe with columns being 24 one hour intervals and indices being the dates for which data is available.

        Input of this method is the filtered dataframe. The output of this method is a dataframe with 24 columns of one hour interval and indices that are dates for which data is available. The columns are datetime.time objects their name being 00:00:00 (defines the 12 a.m.- 1 a.m. interval), 01:00:00 (defines the 1 a.m.- 2 a.m. interval), 02:00:00 (defines the 2 a.m.- 3 a.m. interval) and so on. The indices are datetime.date objects. The value corresponding to a specific column and index is the number of unique customer ID's who moade successful transactions i.e., the number of arrivals on a specific one hour interval in a specific day. If inplace is False then the method returns a copy of the updated dataframe; otherwise updates the input dataframe in place and returns nothing. Default is inplace = False.
        """

        if not inplace:
          data=data.copy()


        newDf=pd.DataFrame(data[["InvoiceDate","CustomerID"]])
        new1=pd.DataFrame({'InvoiceDate':list(pd.Series(pd.date_range('2010-12-01T00',freq='H',periods=8)))})#,'Customers':[np.nan]})
        new2=pd.DataFrame({'InvoiceDate':list(pd.Series(pd.date_range('2011-12-09T13',freq='H',periods=11)))})#,'Customers':[np.nan]})
        newDf=pd.concat([new1,newDf]).reset_index(drop=True)
        newDf=pd.concat([newDf,new2]).reset_index(drop=True)
        newDf['InvoiceDate']=newDf['InvoiceDate'].dt.floor('H')
        newDf=newDf.groupby(pd.Grouper(key='InvoiceDate')).agg({'CustomerID': pd.Series.nunique})
        newDf.reset_index(level=0,inplace=True)
        newDf['Date'] = [d.date() for d in newDf['InvoiceDate']]
        newDf['Time'] = [d.time() for d in newDf['InvoiceDate']]
        newDf.drop(['InvoiceDate'],axis=1,inplace=True)
        newDf=newDf.pivot(index ='Date', columns ='Time',values='CustomerID').fillna(0)

        return newDf


    def drop_columns(self,data,inplace=False,**kwargs):
        """ Drops columns corresponding to one hour intervals in 12 a.m. to 6 a.m. and 8 p.m. to 12 a.m. in the transformed dataframe.

        Input of this method is the transformed dataframe. This method pivots the columns of the dataframe from 6 a.m. to 8 p.m. i.e., 06:00:00 to 19:00:00 by the dropping the columns 00:00:00,01:00:00,...,05:00:00 and 20:00:00,21:00:00,...,23:00:00. If inplace is False then the method returns a copy of the updated dataframe; otherwise updates the input dataframe in place and returns nothing. Default is inplace = False.
        """

        if not inplace:
          data=data.copy()

        col=list(data.columns)[0:6]+list(data.columns)[20:]
        data.drop(columns=col,inplace=True)
        return data

    def subset(self,data,monthly=False,months=[1,2,3],inplace=True, **kwargs):
        """ Produces a dataframe divided into four quarters of 2011 or the months provided.

        Input of this method is the filtered dataframe. In this method rows containing the data of 2010 is dropped.
        If monthly is False this method creates dataframes corresponding to each of quarter of 2011 using week number and returns dataframes of all four quarters. Output['Q1'] produces dataframe of quarter 1 and so on. If monthly is True the method creates dataframe of the months of 2011 provided in the argument and returns dataframe of all these months in the similar fashion as to the quarters. Default months are 1st, 2nd and 3rd i.e, months of the 1st quarter. Default is monthly = False.
        If inplace is False then the method returns a copy of the updated dataframe; otherwise updates the input dataframe in place and returns nothing. Default is inplace = True.
        """

        if not inplace:
            data=data.copy()
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        data.drop(data[data.Date.dt.isocalendar().year==2010].index,inplace=True)
        subset_data={}

        if monthly:
            for month in months:
                subset_data['M'+str(month)]=data.loc[data['Date'].dt.month==month].drop(columns=['index'])
        else:
            data['offset']=pd.DatetimeIndex(data['Date'])+pd.DateOffset(1)
            Q1=data.loc[(data['offset'].dt.isocalendar().week>0) & (data['offset'].dt.isocalendar().week<=13)].copy()
            Q2=data.loc[(data['offset'].dt.isocalendar().week>13) & (data['offset'].dt.isocalendar().week<=26)].copy()
            Q3=data.loc[(data['offset'].dt.isocalendar().week>26) & (data['offset'].dt.isocalendar().week<=39)].copy()
            Q4=data.loc[data['offset'].dt.isocalendar().week>39].copy()

            data.drop(columns=['offset'],inplace=True)
            Q1.drop(columns=['offset'],inplace=True)
            Q2.drop(columns=['offset'],inplace=True)
            Q3.drop(columns=['offset'],inplace=True)
            Q4.drop(columns=['offset'],inplace=True)

            subset_data={'Q1':Q1,'Q2':Q2,'Q3':Q3,'Q4':Q4}
        return subset_data

    def transform_pacf_sequence(self,data,inplace=False):
        """ Creates a timeseries for longest sequence of continuously available data of a time frame.

        Input of this method is dataframe of a time frame. This method detects longest sequence of continuously available data in the given dataframe; for that sequence of data, combines the pivoted time columns and date indices to form timeseries index of timestamp object, flattens the 2D values into 1D values and returns a timeseries data. If inplace is False then the method returns a copy of the updated dataframe; otherwise updates the input dataframe in place and returns nothing. Default is inplace = False.
        """

        if not inplace:
          data=data.copy()

        def longest_seq(df):
          # create mask that indicates sequential pair of days (except the first date)
          df['mask'] = 1
          df.loc[df['Date'] - pd.DateOffset(1) == df['Date'].shift(),'mask'] = 0

          df.loc[df['Date'].dt.day_name()=='Sunday','mask']=0
          # convert mask to numbers - each sequence have its own number
          df['mask'] = df['mask'].cumsum()

          # find largest sequence number and get this sequence
          longest_seq = df.loc[df['mask'] == df['mask'].value_counts().idxmax()].index
          df.drop(columns=['mask'],inplace=True)
          return longest_seq

        def ts_index(df):
          tsi=[]
          for d in df.index:
            for t in df.columns:
              tm=pd.Timestamp.combine(d,t)
              tsi.append(tm)
          return tsi

        def ts_create(df):
          DATA=itertools.chain.from_iterable(df.values)
          ts=pd.Series(DATA,ts_index(df))
          return ts

        data=data.loc[longest_seq(data)]
        data.set_index('Date',drop=True,inplace=True)

        ts=ts_create(data)

        return ts

    def transform_hourly_arrivals_dataset(self,data,lag,monthly=False):
        """ Creates a dataframe with columns being arrivals of previous hours on which arrivals of a specific hour is dependent, arrivals of that specific hour and day, week, month(optional) corresponding to that specific hour.

        Input of this method is timeseries data of a time frame and list of lags for that time frame. In this method, the previous hours on which a specific hour is dependent and their arrivals are calculated using the list of lags. 
        If monthly is False the method returns a dataframe of a quarter with columns being these arrivals, arrival, day, week, month corresponding to that specific hour and index being the hours for which data for the columns are available; otherwise the method returns a dataframe of a month with similar columns excluding the column 'Month'. Default is monthly = False.
        """

        l=max(lag)
        DATA={'h':list(data.index.time)[l:len(data)]}
        df = pd.DataFrame(DATA)
        for i in lag:
          df['arr(h-'+str(i)+')']=list(data)[l-i:len(data)-i]
        df['Day']=(list(data.index.day_name())[l:len(data)])
        df['Week']=pd.Series(list(data.index)[l:len(data)]).apply(lambda x:(x+datetime.timedelta(days=1)).week)
        df['Month']=list(data.index.month)[l:len(data)]
        df['arr(h)']=list(data)[l:len(data)]
        df.set_index('h',inplace=True)
        if monthly:
            df.drop(columns='Month',inplace=True)
        return df
