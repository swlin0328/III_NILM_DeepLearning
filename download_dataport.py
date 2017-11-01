#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pymysql
import pandas as pd
import numpy as np
from collections import OrderedDict

HOST = None
USER = 'nilm'
PWD = None
SAVEFILE = os.path.join('data','III')
DBNAME = None
CURRENT_TIME = '2017-10-30 00:00:00'

def CONNECT(host, user, pwd, dbname,savefile,port=3306):
   
    """ Download data from MySQL into dat files """
    
    try:
        connection = pymysql.connect(host=host,
                             user=user,
                             password=pwd,
                             port=port,
                             db=dbname)
    except:
        print("fail to connect to the  renote database")
        raise
        
    # Get tables in the database schema
    print('quering...')
    sql_query=("SELECT * FROM raw_training_data WHERE reporttime BETWEEN '2017-08-01 00:00:00' AND CURRENT_TIME ")
    stmt = connection.cursor()
    stmt.execute(sql_query)
    database_tables=pd.read_sql(sql_query, connection)                         
    
    # Convert the channelid variable from string to int for using the which function
    database_tables['channelid']=map(int,database_tables['channelid'] )
    # Find all buildings and all channels  within buildings
    Buidlings=list(OrderedDict.fromkeys(database_tables['buildingid']))
    #print (Buidlings)
    Channels=list(OrderedDict.fromkeys(database_tables['channelid']))
    #print (Channels)
    Items = dict.fromkeys(Buidlings,Channels)
    Items
    # Create a function that is analogy to the which function in R
    # To classify the pooling data into channel_i within building_j
    which = lambda lst:list(np.where(lst)[0])

    if not os.path.exists(savefile):
            os.makedirs(savefile)

    for i,j in Items.iteritems():
        # Create the house_i folder
        directory=savefile+'/house_'+str(i)+'/'
        directory=os.path.dirname(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        for k in j:
            TEMP=database_tables
            lst = map(lambda x:x==i, TEMP['buildingid'])
            Building_Index=which(lst)
            TEMP=TEMP.iloc[Building_Index,]
            
            lst_chn = map(lambda x:x==k, TEMP['channelid'])
            Channel_Index=which(lst_chn)
            TEMP=TEMP.iloc[Channel_Index,]
            
            if TEMP.empty:
                TEMP=pd.read_csv(savefile+'/house_'+str(i)+'/'+'channel_1.dat')
                TEMP.iloc[:,1]=0
                Save_load=savefile+'/house_'+str(i)+'/'+'channel_'+str(k+1)+'.dat'
                temp=pd.DataFrame(TEMP)
                temp.to_csv(Save_load, index=False, header=False)
            else:
                Save_load=savefile+'/house_'+str(i)+'/'+'channel_'+str(k+1)+'.dat'
                temp=pd.DataFrame(TEMP.iloc[:,2:4])
                temp.to_csv(Save_load, index=False, header=False)
 
    stmt.close()
    connection.close()
    print ('Done !')
    return  database_tables


if __name__ == '__main__':
    print('Starting...')
    CONNECT( host=HOST, user=USER, pwd=PWD, savefile=SAVEFILE,dbname=DBNAME)
    
  
