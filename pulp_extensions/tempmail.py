# import string
# import random
# from hashlib import md5

import requests
from bs4 import BeautifulSoup

class TempMail(object):
    """
    API Wrapper for service which provides temporary email address.
s.
    :param api_domain: (optional) domain for temp-mail api.
    Default value is ``https://temp-mail.ru/en/`.
    """
    def __init__(self, api_domain='https://temp-mail.ru/en/'):
        super(TempMail, self).__init__()
        self.api_domain = api_domain

    def get_email_address(self):
        s=requests.Session()
        headers={"User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"}
        s.headers.update(headers)
        r=s.get(self.api_domain)
        soup=BeautifulSoup(r.content, "lxml")
        email=soup.find("input",{"id":"mail"})['value']
        return email

        