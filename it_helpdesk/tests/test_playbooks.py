import it_helpdesk
import sys
from it_helpdesk import request_parser, get_request_email as gre
from email import message_from_file, policy
import os
import time
import pytest


helpdesk_dir = os.path.dirname(it_helpdesk.__file__)
email_dir = os.path.join(helpdesk_dir, 'tests', 'test_emails')
email_list = os.listdir(email_dir)
yaml_list = [email.removesuffix('_email.txt') + '.yaml' for email in email_list]
@pytest.mark.parametrize('yaml_file', yaml_list)

def test_playbooks(yaml_file):
        config = gre.load_config(helpdesk_dir)
        email_file = yaml_file.removesuffix('.yaml') + ('_email.txt')
        print('\nSearching for testing emails directory...')
        time.sleep(1)
        assert os.path.exists(email_dir) == True, "Could not find testing emails directory inside it-helpdesk package"
        print(f'Successfully found testing emails directory at {email_dir}')
        time.sleep(1)
        print(f'Using {email_file} for testing...')
        time.sleep(1)
        email_path = os.path.join(email_dir, email_file)
        email_request_type = yaml_file.removesuffix('.yaml')
        with open(email_path, 'r') as email:
            email_msg = message_from_file(email, policy=policy.default)
            test_request = gre.main(email_msg, helpdesk_dir, testing_mode=True)
            test_request_type = config['requests_directory'][test_request[0]]
            assert email_request_type == test_request_type
            
            playbook_dir = os.path.join(test_request[2], 'playbooks')
            print(f'Given playbook directory from it_helpdesk_config.yaml: {playbook_dir}')
            print(f'Searching for {yaml_file} in playbook directory...')
            time.sleep(1)
            assert os.path.exists(os.path.join(playbook_dir, yaml_file)) == True, f"Could not find {test_request_type}.yaml in playbook directory"
            print(f'Successfully found playbook {yaml_file}')
            time.sleep(1)
            
            print(f'Testing {yaml_file} playbook with email {email_file}...')
            sys.stdout = open(os.devnull, 'w')
            output = gre.ansible_run(test_request[0], test_request[1], test_request[2], config, command='--check')
            sys.stdout = sys.__stdout__
            assert output[0] == 'successful', f"Could not run {test_request_type}.yaml playbook on remote server. This is likely due to the remote server being unreachable."
            print(f'Successfully ran {yaml_file} with test email {email_file}')