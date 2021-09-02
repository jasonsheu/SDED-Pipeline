import json
import requests
import pandas as pd
from requests.models import encode_multipart_formdata
from requests.sessions import session

import c2mAPI


# TODO Separate into 2 classes, RagicReader (a single instance of a session), and RagicTools (classless?)
# TODO https://www.ragic.com/intl/en/doc-api/10/Limiting-Entry-Number-%2F-Paging

class RagicReader():

    class AuthenticationError(Exception):
        pass

    # Instance variables
    _SERVER = 'https://www.ragic.com/'


    def __init__(self, api_key: str) -> 'RagicReader':
        '''
            Initialize a ragic API session with an API key
        '''
        
        self.api_key = api_key

        self.session = requests.session()
        self.session.get(self.server)
    
    @classmethod
    def get_api_key(cls, username: str, password: str) -> str:
        '''
            Initialize a ragic API session by authenticating a username
            and password.
        '''

        # Authenticate the username and password
        AUTH_URL = cls._SERVER + 'AUTH' + '?api&v=3'
        payload = {'login_type': 'sessionId', 'u': username, 'p': password}
        response = requests.get(AUTH_URL, payload)

        # Username or password are not correct
        if response.text == '-1':
            raise cls.AuthenticationError
        
        API_KEY_URL = cls._SERVER + 'sims/reg/getAPIKey.jsp'
        response = requests.get(API_KEY_URL, cookies = response.cookies)
        
        api_key = response.text

        return api_key

    def authenticate(self, username: str, password: str):
        AUTH_URL = self._SERVER + 'AUTH'



    def api_request(self, endpoint, payload, server = None):
        # Format endpoint from list or tuple
        if isinstance(endpoint, (list, tuple)):
            endpoint = '/'.join(endpoint)

        if server is None:
            server = self.server

        # Build base url for Ragic API v3
        url = server + endpoint + '?api&v=3'

        response = requests.get(url, params=payload)

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

    def __init__(self, url, api_key):
        self.url = str(url)
        self.api_key = api_key


        self.base_url = 'https://www.ragic.com'
        self.account = 'ccedatabase' #TODO

        self.endpoint_url = '%s?api&APIKey=%s' % (self.url, self.api_key)
    





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
