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


@pytest.mark.parametrize('email_file', email_list)



def test_get_request_type(email_file):
	config = gre.load_config(helpdesk_dir)
	print('\nSearching for testing emails directory...')
	time.sleep(0.5)
	assert os.path.exists(email_dir) == True, "Could not find testing emails directory inside it-helpdesk package"
	print(f'Successfully found testing emails directory at {email_dir}')
	time.sleep(0.5)
	email_path = os.path.join(email_dir, email_file)
	email_request_type = email_file.removesuffix('_email.txt')

	print(f'Attempting to get request type from {email_file}...')
	with open(email_path, 'r') as email:
			subject = message_from_file(email, policy=policy.default)['subject']
			request_type = request_parser.get_request_type(subject, ansible_dir)
			config_lookup = config['requests_directory'][request_type]
			assert config_lookup == email_request_type, f'Failed to get request type from email {email_file}. Determined request type {request_type} did not match expected request type {config_lookup}.'
			print('Successfully got request type from', email_file)
