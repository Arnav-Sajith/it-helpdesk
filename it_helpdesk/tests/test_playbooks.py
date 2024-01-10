import it_helpdesk
from it_helpdesk import request_parser, get_request_email as gre
from email import message_from_file, policy
import os
import time

def test_playbooks():
    helpdesk_dir = os.path.dirname(it_helpdesk.__file__)
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
            print(f'Testing {email_file}')
            time.sleep(1)
            gre.main(email_msg, helpdesk_dir)
            
        time.sleep(1)

test_playbooks()