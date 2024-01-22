import it_helpdesk
from it_helpdesk import request_parser, get_request_email as gre
from email import message_from_file, policy
import os
import time

def delay(time):
    time.sleep(time)

def test_build_and_deploy():
    os.chdir('/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk')
    os.system('poetry build')
    os.system('pip uninstall -y it-helpdesk')
    os.system('pip install dist/it_helpdesk-0.1.2-py3-none-any.whl')

def test_playbooks():
    os.chdir('/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk')
    helpdesk_dir = os.path.dirname(it_helpdesk.__file__)
    print(helpdesk_dir)
    email_dir = os.path.join(helpdesk_dir, 'tests', 'test_emails')
    config = gre.load_config(helpdesk_dir)
    assert os.path.exists(email_dir) == True
    print('Successfully found testing emails')
    time.sleep(1)
    for email_file in os.listdir(email_dir):
        email_path = os.path.join(email_dir, email_file)
        email_request_type = email_file.removesuffix('_email.txt')
        with open(email_path, 'r') as email:
            email_msg = message_from_file(email, policy=policy.default)
            print(f'Testing {email_file} playbook')
            time.sleep(1)
            test_request = gre.main(email_msg, helpdesk_dir, testing_mode=True)
            test_request_type = config['requests_directory'][test_request[0]]
            assert email_request_type == test_request_type
            gre.ansible_run(test_request[0], test_request[1], test_request[2], config, command='--check')

        time.sleep(1)

test_build_and_deploy()
test_playbooks()