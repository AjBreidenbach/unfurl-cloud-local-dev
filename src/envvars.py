import urls
import json

def fetch(session, project_path, environment=None):
    envvars_path = urls.environment_variables_url(project_path)
    response = session.get(envvars_path)

    envvars = []
    if response.ok:
        envvars = json.loads(response.text).get('variables', [])

    if environment is not None:
        envvars = [v for v in envvars if v.get('environment_scope') == environment] + [v for v in envvars if v.get('environment_scope') == '*']

    env_dict = {}

    for v in envvars:
        env_dict[v['key']] = v['value']

    return env_dict
