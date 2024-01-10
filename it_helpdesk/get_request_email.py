import os
from it_helpdesk import request_parser
import yaml
from email.utils import parseaddr
from ansible_runner.config.runner import RunnerConfig
from ansible_runner.runner import Runner

def load_config(helpdesk_dir : str):
    config_path = os.path.join(helpdesk_dir, 'ansible', 'vars', 'it_helpdesk_config.yaml')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        return config


def ansible_run(request_type : int, request_contents : dict, ansible_dir: str, config: dict, **kwargs):
        playbook_name = f"{config['requests_directory'][request_type]}.yaml"
        command = kwargs.get('command', '')
        runner_config = RunnerConfig(private_data_dir = ansible_dir, inventory="./inventory", playbook=f"{os.path.join(ansible_dir, 'playbooks', playbook_name)}", extravars = request_contents, cmdline=f'{command}')
        runner_config.prepare()
        rc = Runner(config=runner_config)
        rc.run()
        return playbook_name

def main(email_msg, helpdesk_dir):
    config = load_config(helpdesk_dir)
    ansible_dir = os.path.join(helpdesk_dir, 'ansible')
    address = parseaddr(email_msg['from'])[1] if parseaddr(email_msg['from'])[1] else parseaddr(email_msg['from'])[0]
    subject = email_msg['subject']
    body = email_msg.get_body(('plain',)).get_content().strip("\n")
    parsed_subject = request_parser.parse_subject_universal(subject, address, body, helpdesk_dir, config)
    request_type = parsed_subject['request_type']
    if request_type == 0:
        request = {'subject': subject, 'body': body, 'from': address}
        ansible_run(request_type, request, ansible_dir, config)
    else:
        parsed_body = request_parser.parse_body_universal(parsed_subject)
        request = {**request_parser.execute_request_universal(parsed_body), 'from': address}
        ansible_run(request['request_type'], request, ansible_dir, config)
        

if __name__ == '__main__':
    main()
