#!/usr/bin/env python
import os
from os import listdir

class House_Appliance_info(object):
       
    def __init__(self):
        self.house_ID = {}
        self.house_channel ={}

    def add_house(self, orignal_name, house_id):
        if orignal_name not in self.house_ID:
            self.house_ID[ orignal_name ] =  house_id
        if house_id not in self.house_channel:
            self.house_channel[ house_id ] = []
            
    def add_appliance(self, house_id, catagory_id, channel_id):
        add_item = [ 'channel_' + str(channel_id) , '000' + catagory_id ]
        if add_item not in self.house_channel[ house_id ]:
            self.house_channel[ house_id ].append(add_item)

    def YAML_Creat(self, house_id_number, foldsave):
        file = open( foldsave + '/building' + str(house_id_number) + '.yaml', 'w')
        House = self.house_channel[ 'house_' + str(house_id_number) ]
        number_channel = len(House)

        for i in range(number_channel):
            i += 1
            if i==1:
                file.write( 'instance : %d\n' %(house_id_number) )
                file.write( 'original_name : house_%d\n' %(house_id_number) )
                file.write( 'elec_meters:\n')
                file.write( ' %d: &emonitor\n' %(i) )
                file.write( '     site_meter" : true\n')
                file.write( '     device_model : eMonitor\n')
                file.write( '     submeter_of: %d\n' %(number_channel) )
                file.write( '     instance : 1\n' )
                file.write( '     meters:[1]\n' )
            else:
                file.write( ' %d: *emonitor\n' %(i) )
        file.write('\n\n')

        file.write('appliances:\n')
        # helper function : convert catagory_id to appliance
        def rename(name):
            if name == '0001':
                name = 'light'
            if name == '0002':
                name = 'television'
            if name == '0003':
                name = 'fridge'
            if name == '0004':
                name = 'air conditioner'
            if name == '0005':
                name = 'bottle warmer'
            if name == '0006':
                name = 'washing machine'
            if name == '1002':
                name = 'fridge'
            if name == '1004':
                name = 'air conditioner'        
            return name

        for i in range(number_channel):
            if i!=0:
                file.write( '- original_name: %s\n' %(rename( House[i][1]) ))
                file.write( '  type: %s\n' %(rename(House[i][1])))
                file.write( '  instance: 1\n')
                file.write( '  meters: [%d]\n' %(i+1) )
                file.write('\n')
        file.close()

    def readme_txt(self, foldsave):
        file = open( foldsave + '/readme.txt', 'w')
        file.write('\n')
        for orignal_name in sorted(self.house_ID.iterkeys()):
            house_id = self.house_ID[orignal_name]
            file.write( './%s : \n' % (house_id) )
            file.write( 'orignal name : %s\n' % (orignal_name) )
            for item in self.house_channel[house_id]:
                file.write( '%s.dat : %s\n' % (item[0], item[1]) )
            file.write( '-------------------------------\n')
        file.write('\n\nDomestic:')
        file.write('0000 : Total\n')
        file.write('0001 : Others\n')
        file.write('0002 : TV\n')
        file.write('0003 : Fridge\n')
        file.write('0004 : AC\n')
        file.write('0005 : Bottle Warmer\n')
        file.write('0006 : Washing Machine\n')
        file.write('\n\nCommerce:')
        file.write('1000 : Total\n')
        file.write('1002 : Fridge\n')
        file.write('1004 : AC\n')
        file.close()
    
    def dataset_yaml(self, foldsave, locality):
        file = open( foldsave + '/dataset.yaml', 'w')
        file.write('name: III\n')
        file.write('creators:\n')
        file.write(' - Fang-Yi Chang\n')
        file.write('publication_date: 2017\n')
        file.write('institution: III\n')
        file.write('contact: fangyichang@iii.org.tw\n')
        file.write('subject: Disaggregated power demand from domestic buildings.\n')
        file.write('number_of_buildings: %d\n' %(len(self.house_ID)))
        file.write('timezone: \'Asia/Taipei\'\n')
        file.write('geo_location:\n')
        file.write(' locality: %s\n' %(locality))
        file.write(' country: Taiwan\n')
        file.close()
    
    def meter_devices(self, foldsave):
        file = open( foldsave + '/meter_devices.yaml', 'w')
        file.write('eMonitor:\n')
        file.write(' model: eMonitor\n')
        file.write(' manufacturer: III\n')
        file.write(' manufacturer_url: https://web.iii.org.tw/default.aspx\n')
        file.write(' description: >\n')
        file.write('   Taiwan\'s regular format\n')
        file.write(' sample_period: 60\n')
        file.write(' max_sample_period: 300\n')
        file.write(' measurements:\n')
        file.write(' - physical_quantity: power\n')
        file.write('   type: active\n')
        file.write('   upper_limit: 500\n')
        file.write('   lower_limit: 0\n')
        file.write(' wireless: false\n\n')
        
        file.write('III_whole_house:\n')
        file.write(' description: >\n')
        file.write('   %d household in III\n'%(len(self.house_ID)))
        file.write(' sample_period: 60\n')
        file.write(' max_sample_period: 300\n')
        file.write(' measurements:\n')
        file.write(' - physical_quantity: power\n')
        file.write('   type: apparent\n')
        file.write('   upper_limit: 5000000\n')
        file.write('   lower_limit: 0\n')
        file.write(' wireless: false\n\n')
        
        
        
                
                           


    


        
            


