import json
import requests
import pandas as pd
from requests.models import encode_multipart_formdata
from requests.sessions import session

import c2mAPI

class RagicReader():

    def __init__(self, API_key):
        '''
            Initialize a ragic API session with an API key
        '''
        self.server = 'https://www.ragic.com'
        self.API_key = API_key

        self.session = requests.session()
        self.session.get(self.server)
    
    def __init__(self, username, password) -> None:
        '''
            Initialize a ragic API session by authenticating a username
            and password.
        '''
        AUTH_endpoint = 'https://www.ragic.com/AUTH'
        payload = {'v': '3', 'u': username, 'p': password, 'login_type': 'sessionId'}
        response = requests.get(AUTH_endpoint, params=payload)
        session_ID = response.cookies

        API_endpoint = 'https://www.ragic.com/sims/reg/getAPIKey.jsp'
        response = requests.get(API_endpoint, cookies=session_ID)
        API_key = response.text

        self.__init__(API_key)

    def ragic_api_request(self, endpoint, payload):
        url = self.server + endpoint + '?api'
        response = requests.get(endpoint, params=payload)
        return response





    def build_endpoint_url(self): #TODO
        '''
        Build the URL endpoint for the initially-specified table
        for v3, this looks like 
        
        For info on how to find Ragic API endpoints, see:
        https://www.ragic.com/intl/en/doc-api/7/Finding-API-endpoints
        '''

        pass



class RagicTools():
    def __init__(self, tab_folder, sheet_index, api_key):
        self.tab_folder = str(tab_folder)
        self.sheet_index = str(sheet_index)
        self.api_key = api_key


        self.base_url = 'https://www.ragic.com'
        self.account = 'ccedatabase' #TODO

        self.endpoint_url = 'https://www.ragic.com/ccedatabase/%s/%s?api&APIKey=%s' % (self.tab_folder, self.sheet_index, self.api_key)



    def log_in(self, username, password): #TODO
        payload = [('u', username), ('p', password), ('login_type', 'sessionId'), ('api','')]
        
        self.endpoint_url = 'https://www.ragic.com/AUTH?api&APIKey=%s' % (self.tab_folder, self.sheet_index, self.api_key)

        r = requests.get("https://www.ragic.com/AUTH", params=payload)


    def get_table(self):
        '''
        gets table passed into constructor
        '''
        r = requests.get(self.endpoint_url)

        print("Retrieving table at:", self.endpoint_url)
        
        # Dump json (dict) object into a string
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

        r = requests.post(self.endpoint_url, files = entry)
        return r.json()

    def delete_entry(self, row_id):
        '''
        deletes row in current table in
        '''
        row_id = str(row_id)
        endpoint_url = 'https://www.ragic.com/ccedatabase/%s/%s/%s?api&APIKey=%s' % (self.tab_folder, self.sheet_index, row_id, self.api_key)
        r = requests.delete(endpoint_url)
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
        endpoint_url = 'https://www.ragic.com/ccedatabase/%s/%s/%s?api&APIKey=%s' % (self.tab_folder, self.sheet_index, row_id, self.api_key)
        r = requests.post(endpoint_url, updated_entry)
        return r.json()

    def get_sheet_index(self):
        return self.sheet_index
    def get_group(self):
        return self.tab_folder


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
