import requests
import re
import urls
import envvars

authenticity_token_regex = re.compile('name="csrf-token"\s+content="(([A-Za-z0-9+/=])+)"')

class UnfurlCloudSession:
    def __init__(self):
        self.session = requests.session()
        self.authenticity_token = self.fetch_authenticity_token()


    def fetch_authenticity_token(self):
        sign_in_page = self.session.get(urls.SIGN_IN_URL)
        token = authenticity_token_regex.search(sign_in_page.text).groups()[0]
        return token

    def fetch_environment_variables(self, project_path=None, environment=None):
        if project_path is None:
            project_path = "%s/dashboard" % self.username
        return envvars.fetch(self.session, project_path, environment)

    #TODO throw an error if this fails?
    def sign_in(self, username, password):
        self.username = username
        form_data = {
                "authenticity_token": self.authenticity_token,
                "user[login]": username,
                "user[password]": password
                }
        response = self.session.post(urls.SIGN_IN_URL, data=form_data)
