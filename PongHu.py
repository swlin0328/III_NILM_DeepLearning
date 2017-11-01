#!/usr/bin/env python

import os
from os import listdir
import pandas as pd

from dataprocess import House_Appliance_info

FOLDER_RAW = os.path.join( 'data' , 'HEMS' , 'PongHu_Raw' )
FOLDER = os.path.join( 'data' , 'HEMS' , 'PongHu' )

def main():
    filenames = [ filename for filename in listdir(FOLDER_RAW) if filename.endswith('.csv') and filename.startswith('hems') ]
    filenames = sorted( filenames )
    House_Appliance = House_Appliance_info.House_Appliance_info()

    if not os.path.exists( FOLDER ):
        print "Creating ./HEMS/PongHu folder ..."
        os.makedirs(FOLDER)

    METADATA = os.path.join(FOLDER, 'metadata')
    if not os.path.exists( METADATA ):
        print "Creating Metadata folder ..."
        os.makedirs(METADATA)
    
    for building, filename in enumerate(filenames):
        print "Processing", filename, "..."
        house_id = 'house_' + str( building+1 )
        House_Appliance.add_house( filename, house_id)
        file = pd.read_csv( os.path.join( FOLDER_RAW, filename) )

        savefolder = os.path.join( FOLDER, 'house_' + str( building+1 ) )
        if not os.path.exists( savefolder ):
            print "Creating",savefolder, "folder ..."
            os.makedirs(savefolder)

        for channel, channelid in enumerate( sorted( file.groupby( ['channelid'] ).groups )):
            catagory_id = str(channelid)
            channel_id = str( channel+1 )
            House_Appliance.add_appliance( house_id, catagory_id, channel_id )
            savefile =  savefolder + '/' + 'channel_' + channel_id + '.dat'
            channel_data = file.groupby( ['channelid'] ).get_group( channelid )
            channel_data = channel_data[[ 'reporttime', 'w' ]]
            channel_data.to_csv( savefile, index=False, header=False)
        
        print "Creating building", building+1, ".yaml ..."
        house_id_number = building + 1 
        House_Appliance.YAML_Creat(house_id_number, METADATA)    

    print "Creating dataset.yaml and meter_devices ..."
    House_Appliance.dataset_yaml(METADATA, 'PongHu')
    House_Appliance.meter_devices(METADATA)
    print "Creating readme.txt ..."
    House_Appliance.readme_txt(FOLDER)
    print "Done !"   

if __name__ == '__main__':
    main()
    #filenames = [ filename for filename in listdir(FOLDER_RAW) if filename.endswith('.csv') and filename.startswith('hems') ]
    #filenames = sorted( filenames )
    #Creat_YAML( filenames )