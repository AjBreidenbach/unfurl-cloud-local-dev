import sys
import subprocess
import shutil
import tempfile
import urls
from pathlib import Path
import os
import json

class UnfurlCommandRunner():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.dashboard_dir = tempfile.mkdtemp()
        self.dashboard_git_url = urls.dashboard_url(username, password)

    def clone_dashboard(self):
        completed_clone = subprocess.run(['git', 'clone', self.dashboard_git_url, '.'], cwd=self.dashboard_dir)
        return subprocess.run(['git', 'checkout', 'main'], cwd=self.dashboard_dir)

    def lookup_deployment_variables(self, deploy_path):
        environments_content = Path(os.path.join(self.dashboard_dir, 'environments.json')).read_text()
        environments_dict = json.loads(environments_content)
        return environments_dict['DeploymentPath'][deploy_path]['pipeline']['variables']

    def unfurl_clone(self, env):
        if Path(os.path.join(self.dashboard_dir, env.get('DEPLOY_PATH'), 'ensemble.json')).exists(): return
        args = ['unfurl', '--home', '""', 'clone', '--existing', '--overwrite', '--mono', '--use-environment', env.get('DEPLOY_ENVIRONMENT'), '--skeleton', 'dashboard', env.get('BLUEPRINT_PROJECT_URL'), env.get('DEPLOY_PATH')]
        return subprocess.run(args, cwd=self.dashboard_dir, env=env)

    def unfurl_deploy(self, env):
        workflow = env.get('WORKFLOW', 'deploy')
        #unfurl_home_command = subprocess.run(['unfurl', 'home'], capture_output=True)
        #unfurl_home = unfurl_home_command.stdout.decode('utf-8').strip()
        #unfurl = shutil.which('unfurl')
        #sudo_env = {'PYTHONPATH': ':'.join(sys.path)}
        #sudo_env.update(env)
        args = ['unfurl', '-vvv', workflow, '--approve', env.get('DEPLOY_PATH')]
        #args = ['sudo', '-E', unfurl, '-vvv', '--home', unfurl_home, workflow, '--approve', env.get('DEPLOY_PATH')]
        return subprocess.run(args, cwd=self.dashboard_dir, env=env)

    def unfurl_export(self, env):
        args = ['unfurl', '--home', '""', 'export', env.get('DEPLOY_PATH')]
        export_command = subprocess.run(args, cwd=self.dashboard_dir, env=env, capture_output=True)

        print(export_command.stderr.decode('utf-8'))

        if export_command.returncode == 0:
            ensemble = os.path.join(self.dashboard_dir, env.get('DEPLOY_PATH'), 'ensemble.json')
            Path(ensemble).write_bytes(export_command.stdout)

        return export_command

    def unfurl_commit(self, env):
        deploy_path = env.get('DEPLOY_PATH')
        workflow = env.get('WORKFLOW', 'deploy')
        args = ['unfurl', 'commit' , '-m"%s from local development script for %s"' % (workflow, deploy_path), deploy_path]
        return subprocess.run(args, cwd=self.dashboard_dir, env=env)

    def git_pull(self, env=None):
        args = ['git', 'pull', '--no-rebase']
        return subprocess.run(args, cwd=self.dashboard_dir, env=env)


    def git_push(self, env=None):
        args = ['git', 'push', '-o', 'ci.skip']
        return subprocess.run(args, cwd=self.dashboard_dir, env=env)
