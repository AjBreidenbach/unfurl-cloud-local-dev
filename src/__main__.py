import sys

import session
import unfurl_commands
import os

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

def environment_name_from_deploy_path(deploy_path):
    splits = deploy_path.split('/')
    return splits[1]

def verify_subcommand(command_name, completed_process):
    if completed_process is None: return
    if completed_process.returncode != 0:
        print(completed_process.args)
        print('%s failed with %' % (command_name, completed_process.returncode))
        sys.exit(completed_process.returncode)
    else: print('finished', command_name)

def main():
    deploy_path = sys.argv[1]
    environment_name = environment_name_from_deploy_path(deploy_path)
    uf_commands = unfurl_commands.UnfurlCommandRunner(USERNAME, PASSWORD)

    uf_commands.clone_dashboard()
    deployment_variables = uf_commands.lookup_deployment_variables(deploy_path)
    uf_session = session.UnfurlCloudSession()
    uf_session.sign_in(USERNAME, PASSWORD)

    environment_variables = uf_session.fetch_environment_variables('%s/dashboard' % USERNAME)

    environment_variables.update(deployment_variables)
    environment_variables.update(os.environ)

    verify_subcommand('Unfurl clone', uf_commands.unfurl_clone(environment_variables))
    verify_subcommand('Unfurl deploy', uf_commands.unfurl_deploy(environment_variables))
    verify_subcommand('Unfurl export', uf_commands.unfurl_export(environment_variables))
    verify_subcommand('Unfurl commit', uf_commands.unfurl_commit(environment_variables))

    environment_variables['WORKFLOW'] = 'undeploy'

    verify_subcommand('Unfurl undeploy', uf_commands.unfurl_deploy(environment_variables))
    verify_subcommand('Unfurl export', uf_commands.unfurl_export(environment_variables))
    verify_subcommand('Unfurl commit', uf_commands.unfurl_commit(environment_variables))

    #verify_subcommand('Git pull', uf_commands.git_pull(environment_variables))
    #verify_subcommand('Git push', uf_commands.git_push(environment_variables))

if __name__ == '__main__':
    main()
