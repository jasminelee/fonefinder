import requests
import phonenumbers
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

INVALID_US_NUMBER = 'Phone number is not a valid US number'
NO_RECORDS_FOUND = 'No records found for that phone number'
class FoneFinder:
    """
    Parent class to be used to find information on a phone number, i.e. carrier and city
    """
    def __init__(self, phone_number):
        self.phone_number = self.validate(phone_number)
        self.area_code, self.prefix, self.line_number = self.__parse_number(phone_number)
        self.url = f'http://www.fonefinder.net/findome.php?npa={self.area_code}&nxx={self.prefix}&thoublock={self.line_number}&usaquerytype=Search+by+Number&cityname='
        self.response = requests.get(self.url)
        self.info = self.__parse_page(self.response)

    def validate(self, phone_number):
        phone_number = re.sub("[^0-9]", "", phone_number)
        if not phonenumbers.is_valid_number(phonenumbers.parse(phone_number, 'US')):
            raise ValueError(INVALID_US_NUMBER)
        else:
            return phone_number

    def __parse_number(self, phone_number):
        area_code = phone_number[0:3]
        prefix = phone_number[3:6]
        line_number = phone_number[6:]
        return area_code, prefix, line_number

    def __parse_page(self, response_payload):
        if self.response.status_code != 200:
            raise HTTPError(self.url, self.response.status_code, 'Request to FoneFinder did not succeed', self.response.headers, self.response.fp)
        html_page_text = BeautifulSoup(response_payload.content, 'html.parser')
        if 'Sorry, no records found' in html_page_text.body.strings:
            raise ValueError(NO_RECORDS_FOUND)
        city, state, carrier, telco_type = list(html_page_text.body.find_all('a')[3].strings)
        info = {
            'city': city,
            'state': state,
            'carrier': carrier,
            'telco_type': telco_type,
            'url': self.url,
            'area_code': self.area_code,
            'prefix': self.prefix,
            'line_number': self.line_number,
        }
        return info
