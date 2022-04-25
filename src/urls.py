import os
BASE_URL = os.getenv('BASE_URL')
SIGN_IN_URL = BASE_URL + '/users/sign_in'

def environment_variables_url(project_path):
    return BASE_URL + "/%s/-/variables" % project_path

# TODO acknowledge group
def dashboard_url(username, password=None, group=None):
    base_url = BASE_URL
    if password is not None:
        base_url = base_url.replace('//', '//%s:%s@' % (username, password))
    return base_url + "/%s/dashboard" % username
