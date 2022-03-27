import requests

# TODO https://www.ragic.com/intl/en/doc-api/10/Limiting-Entry-Number-%2F-Paging

# Tools for dealing with the Ragic API
class RagicTools():

    def __init__(self, tab_folder, sheet_index, api_key):
        self.tab_folder = str(tab_folder)
        self.sheet_index = str(sheet_index)
        self.api_key = api_key


        self.base_url = 'https://www.ragic.com'
        self.account = 'ccedatabase' #TODO

        self.endpoint_url = 'https://www.ragic.com/ccedatabase/%s/%s?api&APIKey=%s' % (self.tab_folder, self.sheet_index, self.api_key)




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
