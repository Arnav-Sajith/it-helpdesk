import it_helpdesk
from it_helpdesk import request_parser, get_request_email as gre
from email import message_from_file, policy
import os
import pytest
import time


helpdesk_dir = os.path.dirname(it_helpdesk.__file__)
ansible_dir = os.path.join(helpdesk_dir, 'ansible')
email_dir = os.path.join(helpdesk_dir, 'tests', 'test_emails')
email_list = os.listdir(email_dir)
config = gre.load_config(helpdesk_dir)


@pytest.mark.parametrize('email_file', email_list)



def test_get_request_type(email_file):
	assert os.path.exists(email_dir) == True
	email_path = os.path.join(email_dir, email_file)
	email_request_type = email_file.removesuffix('_email.txt')
	assert os.path.exists(email_path) == True
	print('Attempting to get request type from ', email_file)
	with open(email_path, 'r') as email:
			subject = message_from_file(email, policy=policy.default)['subject']
			request_type = request_parser.get_request_type(subject, ansible_dir)
			config_lookup = config['requests_directory'][request_type]
			assert config_lookup == email_request_type
			print('Successfully got request type from ', email_file)
