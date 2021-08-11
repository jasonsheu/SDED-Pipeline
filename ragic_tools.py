import requests
import config
from api import c2mAPI
import pandas as pd

class RagicTools():
    def __init__(self, table_id, group_name, api):
        self.table_id = str(table_id)
        self.group_name = str(group_name)
        self.api = api
        self.url = 'https://www.ragic.com/ccedatabase/%s/%s?api&APIKey=%s' % (self.group_name, self.table_id, self.api)
    def get_table(self):
        '''
        gets table passed into constructor
        '''
        r = requests.get(self.url)
        return r.json()

    def add_entry(self, entry):
        '''
        entry must look like this:
        files = {
            '1000114': (None, '8'),
            '1000115': (None, 'column 1-2-3'),
            '1000116': (None, 'column 2-2'),
            '1000117': (None, 'column 3-2')
        }
        where the keys are the column ids that can be found in ragic
        adds entry to table
        '''

        r = requests.post(self.url, files = entry)
        return r.json()

    def delete_entry(self, row_id):
        '''
        deletes row in current table in
        '''
        row_id = str(row_id)
        url = 'https://www.ragic.com/ccedatabase/%s/%s/%s?api&APIKey=%s' % (self.group_name, self.table_id, row_id, self.api)
        r = requests.delete(url)
        return r.json()

    def update_entry(self, row_id, updated_entry):
        '''
        updates given row with new data in group
        entry must look like this:
        updated_entry = {
            '1000114': (None, '9'),
            '1000115': (None, 'updated'),
            '1000116': (None, 'from'),
            '1000117': (None, 'script')
        }

        '''
        row_id = str(row_id)
        url = 'https://www.ragic.com/ccedatabase/%s/%s/%s?api&APIKey=%s' % (self.group_name, self.table_id, row_id, self.api)
        r = requests.post(url, updated_entry)
        return r.json()

    def get_table_id(self):
        return self.table_id
    def get_group(self):
        return self.group_name


class RagicMailer:

    def __init__(self, file, username, password):

        self.df = pd.read_csv(file)
        self.username = username
        self.password = password


    def send_all_mail(self, filename, path):
        c2m = c2mAPI.c2mAPIBatch(self.username, self.password, "0") #change to 1 for production
        c2m.setFileName(filename, path) #set the name ane file path for batch

        #change to appropriate address and options
        po = c2mAPI.printOptions('Letter 8.5 x 11','Next Day','Address on Separate Page','Full Color','White 24#','Printing both sides','First Class','#10 Double Window')
        ad = c2mAPI.returnAddress("Jason Sheu","SDED","3855 Nobel Drive","apt 2101","La Jolla","CA","92122")

        addList = [] #field names cannot change
        for i in range(len(self.df)):
            addList.append(self.df.iloc[i].to_dict())

        return addList

#         c2m.addJob("1","2",po,ad,addList)
#         print(c2m.runAll().text)

    def send_specific(self, name, organization , address1, address2 , address3 , city, state, postalCode, country, filename, path):
        c2m = c2mAPI.c2mAPIBatch(self.username, self.password, "1") #change to 1 for production
        c2m.setFileName(filename, path) #set the name ane file path for batch

        #change to appropriate address and options
        po = c2mAPI.printOptions('Letter 8.5 x 11','Next Day','Address on Separate Page','Full Color','White 24#','Printing both sides','First Class','#10 Double Window')
        ad = c2mAPI.returnAddress("Jason Sheu","SDED","3855 Nobel Drive","apt 2101","La Jolla","CA","92122")

        addList = []
        address = {'name': name,
                   'organization': organization,
                   'address1': address1,
                   'address2': address2,
                   'address3': address3,
                   'city': city,
                   'state': state,
                   'postalCode': postalCode,
                   'country':country}
        addList.append(address)
        c2m.addJob("1","2",po,ad,addList) # start page, stop page

        #this line sends the mail through the api
        print(c2m.runAll().text)
