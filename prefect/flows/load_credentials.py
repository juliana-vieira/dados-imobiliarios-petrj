from prefect_aws import AwsCredentials
from dotenv import load_dotenv
import os

class Credentials:

    def __init__(self):
        self.get_cookies()
        self.get_headers()
        self.get_aws_credentials()
        self.get_base_url()
        load_dotenv()

    def get_cookies(self):

        self.cookies = {
            'r_id': os.getenv('R_ID'),
            'nl_id': os.getenv('NL-Id'),
            'cf_clearance': os.getenv('CF-CLEARANCE'),
            '_cfuvid': os.getenv('_CFUVID'),
            'TestAB_Groups': os.getenv('TESTAB_GROUPS'),
            '__cf_bm': os.getenv('__CF_BM'),
        }

    def get_headers(self):

        self.headers = {
            'User-Agent': os.getenv('USER-AGENT'),
            'Accept': os.getenv('ACCEPT'),
            'Accept-Language': os.getenv('ACCEPT-LANGUAGE'),
            'Referer': os.getenv('REFERER'),
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0, i',
        }

    def get_aws_credentials(self):

        self.aws_credentials = AwsCredentials.load("aws-credentials")

    def get_base_url(self):
    
        self.base_url = "https://www.olx.com.br/imoveis/aluguel/estado-rj/serra-angra-dos-reis-e-regiao/petropolis?ret=1020&ret=1040"