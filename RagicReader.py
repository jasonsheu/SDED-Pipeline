import requests

# RagicReader (a single instance of a session)
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

