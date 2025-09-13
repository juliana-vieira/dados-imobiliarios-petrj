from prefect.blocks.system import Secret
from prefect_aws import AwsCredentials
from prefect.variables import Variable

class Credentials:

    def __init__(self):
        self.get_cookies()
        self.get_headers()
        self.get_aws_credentials()
        self.get_base_url()

    def get_cookies(self):

        self.cookies = {
            'r_id': Secret.load('r-id').get(),
            'nl_id': Secret.load('nl-id').get(),
            'cf_clearance': Secret.load('cf-clearance').get(),
            '_cfuvid': Secret.load('cfuvid').get(),
            'TestAB_Groups': Secret.load('testab-groups').get(),
            '__cf_bm': Secret.load('cf-bm').get(),
        }

    def get_headers(self):

        self.headers = {
            'User-Agent': Secret.load('user-agent').get(),
            'Accept': Secret.load('accept').get(),
            'Accept-Language': Secret.load('accept-language').get(),
            'Referer': Secret.load('referer').get(),
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
    
        self.base_url = Variable.get("base_url")