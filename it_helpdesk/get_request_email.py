from sys import stdin
import os
import email
from it_helpdesk import request_parser
import yaml
from email.policy import default
from email.utils import parseaddr
from ansible_runner.config.runner import RunnerConfig
from ansible_runner.runner import Runner

def ansible_run(request_type : int, request_contents : dict, helpdesk_dir: str):
    os.chdir(helpdesk_dir)
    with open('vars/it_helpdesk_config.yaml', 'r') as config:
        print('working')
        config_file = yaml.safe_load(config)
        runner_config = RunnerConfig(private_data_dir = helpdesk_dir, inventory="./inventory", playbook=f"{helpdesk_dir}/{config_file['requests_directory'][request_type]}.yaml", extravars = request_contents)
        runner_config.prepare()
        rc = Runner(config=runner_config)
        rc.run()

def main(email_msg, helpdesk_dir):
    address = parseaddr(email_msg['from'])[1] if parseaddr(email_msg['from'])[1] else parseaddr(email_msg['from'])[0]
    body = email_msg.get_body(('plain',)).get_content().strip("\n")
    parsed_subject = request_parser.parse_subject_universal(email_msg['subject'], address, body, helpdesk_dir)
    parsed_body = request_parser.parse_body_universal(parsed_subject)
    request = {**request_parser.execute_request_universal(parsed_body), 'from': address}
    ansible_run(request['request_type'], request, helpdesk_dir)
        

if __name__ == '__main__':
    main()
