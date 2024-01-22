import it_helpdesk
from it_helpdesk import request_parser, get_request_email as gre
from email import message_from_file, policy
import os
import time
import pytest

helpdesk_dir = os.path.dirname(it_helpdesk.__file__)
print(helpdesk_dir)
email_dir = os.path.join(helpdesk_dir, 'tests', 'test_emails')
email_list = os.listdir(email_dir)
config = gre.load_config(helpdesk_dir)
assert os.path.exists(email_dir) == True
print('Successfully found testing emails directory')
time.sleep(1)
@pytest.mark.parametrize('email_file', email_list)



def test_playbooks(email_file):
        email_path = os.path.join(email_dir, email_file)
        email_request_type = email_file.removesuffix('_email.txt')
        with open(email_path, 'r') as email:
            email_msg = message_from_file(email, policy=policy.default)
            print(f'Testing {email_request_type}.yaml playbook for email {email_file}')
            test_request = gre.main(email_msg, helpdesk_dir, testing_mode=True)
            test_request_type = config['requests_directory'][test_request[0]]
            assert email_request_type == test_request_type
            output = gre.ansible_run(test_request[0], test_request[1], test_request[2], config, command='--check')
            assert output[0] == 'successful'
