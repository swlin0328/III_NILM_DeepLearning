#!/usr/bin/env python

import os
from os import listdir
import argparse
import pymysql
import pandas as pd
from time import strftime
from sys import stdout

from dataprocess import House_Appliance_info

commercial_or_not = False
Groupby = None
HOST = None
USER = None
PWD = None
PORT = 3306
DBNAME = None
SAVEFILE = None
CURRENT_TIME = strftime('%Y-%m-%d %H:%M:%S')


def main():
    parse_args()   
    whether_commercial()
    print('quering......')
    table = query()
    table.to_csv( SAVEFILE + '/table.csv')

    METADATA = os.path.join(SAVEFILE, 'metadata')
    if not os.path.exists( METADATA ):
        os.makedirs(METADATA) 

    House_Appliance = House_Appliance_info.House_Appliance_info()
    for item, building in enumerate( sorted(table.groupby( ['buildingid'] ).groups)):
        orignal_name = building
        house_id = 'house_' + str(item+1)
        House_Appliance.add_house(orignal_name, house_id)
        building_data = table.groupby(['buildingid']).get_group(building)
        savefolder = SAVEFILE + '/house_' + str(building) + '/'
        if not os.path.exists(savefolder):
            print "Creating", savefolder, "folder"
            os.makedirs(savefolder)

        for channel_id, catagory_id in enumerate(sorted(building_data.groupby(Groupby).groups)):
            channel_id = str( channel_id+1 )
            savefile =  savefolder + '/' + 'channel_' + channel_id + '.dat'
            House_Appliance.add_appliance( house_id, catagory_id, channel_id )
            channel_data = building_data.groupby( Groupby ).get_group( catagory_id )
            channel_data = channel_data[[ 'reporttime', 'w' ]]
            channel_data.to_csv( savefile, index=False, header=False)

        print "Creating building", int(building)+1, ".yaml ..."
        house_id_number = int(building)
        print(house_id_number)
        House_Appliance.YAML_Creat(house_id_number, METADATA)    

    print "Creating dataset.yaml and meter_devices ..."
    House_Appliance.dataset_yaml(METADATA, 'Taipei')
    House_Appliance.meter_devices(METADATA)
    print "Creating readme.txt ..."
    House_Appliance.readme_txt(SAVEFILE)
    print "Done !"   
    

def parse_args():
    global commercial_or_not 
    parser = argparse.ArgumentParser()
    optional_named_arguments = parser.add_argument_group('optional named arguments')
    optional_named_arguments.add_argument('-c', '--commercial',
                                          help='Flag for commercial dataset',
                                          action='store_true')
    args = parser.parse_args()
    commercial_or_not = args.commercial
    if commercial_or_not is not None:
        commercial_or_not = True

def whether_commercial():
    global Groupby, HOST, USER, PWD, DBNAME, SAVEFILE
    if not commercial_or_not:
        print "The type of the dataset is domestic"
        Groupby = ['channelid']
        #HOST = '140.92.60.81'
        HOST = '125.227.5.116'
        USER = 'nilm'
        PWD = '1qaz@WSX'
        DBNAME = 'ddms_dev'
        SAVEFILE = os.path.join('data','III')
    else:
        print "The type of the dataset is commerce"
        Groupby = ['channelid','deviceid']
        HOST = '223.27.48.230'
        USER = 'tkfc'
        PWD = '1qaz@WSX'
        DBNAME = 'iii_bees_all'
        SAVEFILE = os.path.join('data','III_Commercial')
    
    if not os.path.exists( SAVEFILE ):
        os.makedirs( SAVEFILE ) 

def query():
    stdout.flush()
    connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PWD,
                             port=3306,
                             db=DBNAME)
    sql_query = ("SELECT * FROM field_raw_training_data WHERE reporttime BETWEEN '2017-08-01 00:00:00' AND CURRENT_TIME ")
    stmt = connection.cursor()
    stmt.execute(sql_query)
    table = pd.read_sql(sql_query, connection) 
    return table


                                          
if __name__ == '__main__':
    main()

