import requests
import json
from random import randint
from logging import error

class MailTM:
    __BASE_URL = 'https://api.mail.tm'
    
    __BASE_HEADERS = {
        'Content-Type':'application/json', 
        'accept':'application/json'
    }

    class __Endpoints():
        REGISTER = '/accounts'
        MESSAGES = '/messages'
        DOMAINS  = '/domains'
        TOKEN    = '/token'

    __make_url = lambda self, endpoint: self.__BASE_URL + endpoint

    __request_successful = lambda self, sc: sc in [200, 201, 204]

    def __random_string(self, min=10, max=25):
        """
        Generate a random string of digits and lowercase
        characters of length between `min` and `max`.
        """
        length = randint(min, max)
        result = ""
        for _ in range(length):
            d = randint(0, 2) == 0
            # Lowercase letters range = [97, 122]
            # Digits range = [48, 57]
            result += chr(randint(48, 57)) if d else chr(randint(97, 122))
        return result

    def fetch_domains(self):
        """
        Returns the list of currently available domains.
        """
        url = self.__make_url(self.__Endpoints.DOMAINS)

        # Its very unusual to have more than 1 page of available domains.
        response = requests.get(url, params={'page':1})

        if not self.__request_successful(response.status_code):
            fn = self.fetch_domains.__name__
            error(f'{fn}:Bad status code ({response.status_code})')
            return None

        response_dict = json.loads(response.text)
        domains_list  = [_['domain'] for _ in response_dict['hydra:member']]

        return domains_list
    
    def register(self, address, password):
        url  = self.__BASE_URL + self.__Endpoints.REGISTER
        data = json.dumps({'address':address, 'password':password})

        response = requests.post(url, data=data, headers=self.__BASE_HEADERS)

        if not self.__request_successful(response.status_code):
            fn = self.fetch_domains.__name__
            error(f'{fn}:Bad status code ({response.status_code})')
            return None

        return address, password

    def register_random(self):
        """
        Generate and register a new random (address, password) pair.
        """
        local_part        = self.__random_string() 
        password          = self.__random_string()
        available_domains = self.fetch_domains()

        if len(available_domains) == 0:
            fn = self.fetch_domains.__name__
            error(f'{fn}:No available domains.')
            return None

        random_i = randint(0, len(available_domains)-1)
        domain   = available_domains[random_i]
        address  = f'{local_part}@{domain}' 

        return self.register(address, password)

    def bearer_token(self, address, password):
        url  = self.__make_url(self.__Endpoints.TOKEN)
        data = json.dumps({'address':address, 'password':password})

        response = requests.post(url=url, headers=self.__BASE_HEADERS, data=data)

        if not self.__request_successful(response.status_code):
            fn = self.fetch_domains.__name__
            error(f'{fn}:Bad status code ({response.status_code})')
            return None

        response_dict = json.loads(response.text)

        return response_dict['token']

    def fetch_emails(self, token):
        """
        Get a dictionary of all received emails.
        """
        # Adding the auth token.
        headers = self.__BASE_HEADERS
        headers['Authorization'] = f'Bearer {token}'

        url = self.__make_url(self.__Endpoints.MESSAGES)

        response = requests.get(url, params={'page':1}, headers=headers)

        if not self.__request_successful(response.status_code):
            fn = self.fetch_domains.__name__
            error(f'{fn}:Bad status code ({response.status_code})')
            return None

        response_dict = json.loads(response.text)
        return response_dict