from sys import stdin
import os
import email
import request_parser
import yaml
from email.policy import default
from email.utils import parseaddr
from ansible_runner.config.runner import RunnerConfig
from ansible_runner.runner import Runner



def ansible_run(request_type : int, request_contents : dict, install_path):
    os.chdir(install_path)
    with open('vars/it_helpdesk_config.yaml', 'r') as config:
        config_file = yaml.safe_load(config)
        runner_config = RunnerConfig(private_data_dir = install_path, inventory="./inventory", playbook=f"{install_path}/{config_file['requests_directory'][request_type]}.yaml", extravars = request_contents)
        runner_config.prepare()
        rc = Runner(config=runner_config)
        rc.run()

def main():
    with open('./sample.txt', 'r') as fp:
        install_path = os.path.join(os.path.expanduser('~'), 'it-helpdesk', 'ansible')
        email_msg = email.message_from_file(fp, policy=default)
        address = parseaddr(email_msg['from'])[1] if parseaddr(email_msg['from'])[1] else parseaddr(email_msg['from'])[0]
        body = email_msg.get_body(('plain',)).get_content().strip("\n")
        parsed_subject = request_parser.parse_subject_universal(email_msg['subject'], address, body, install_path)
        parsed_body = request_parser.parse_body_universal(parsed_subject)
        request = {**request_parser.execute_request_universal(parsed_body), 'from': address}
        ansible_run(request['request_type'], request, install_path)
        

if __name__ == '__main__':
    main()