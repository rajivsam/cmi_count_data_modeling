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
    
    def filter(self, data,inplace=False,**kwargs):
        if not inplace:
          data=data.copy()
        data=data.dropna(subset=['CustomerID'])
        data.drop(index=data.loc[data['InvoiceNo'].str.match(r'^C.*')==True].index,inplace=True)
        return data
    
    def transform(self,data,inplace=False, **kwargs):
        if not inplace:
          data=data.copy()
        
        ## Creating Date and Hour columns from the timestamp InvoiceDate
        ## Here Hour is the truncated time of the day. if the time is hh:mm:ss, Hour is hh only.
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
      if not inplace:
        data=data.copy()
      
      col=list(data.columns)[0:6]+list(data.columns)[20:]
      data.drop(columns=col,inplace=True)
      return data
    
    def subset(self,data,inplace=True, **kwargs):
        if not inplace:
            data=data.copy()
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        data.drop(data[data.Date.dt.isocalendar().year==2010].index,inplace=True)
        
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

    def transform_hourly_arrivals_dataset(self,data,lag):
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
        return df
