import it_helpdesk
import os
import time
import pytest
from it_helpdesk import request_parser, get_request_email as gre
from email import message_from_file, policy

helpdesk_dir = os.path.dirname(it_helpdesk.__file__)
email_dir = os.path.join(helpdesk_dir, 'tests', 'test_emails')
email_list = os.listdir(email_dir)
config = gre.load_config(helpdesk_dir)

@pytest.mark.parametrize('email_file', email_list)


def test_parse_subject(email_file):
   
    print('\nSearching for testing emails directory...')
    time.sleep(0.5)
    assert os.path.exists(email_dir) == True, "Could not find testing emails directory inside it-helpdesk package"
    print(f'Successfully found testing emails directory at {email_dir}')
    time.sleep(0.5)

    email_path = os.path.join(email_dir, email_file)
    print(f'Using {email_file} for testing...')
    assert os.path.exists(email_path) == True, f"Could not find {email_file} in email directory"
    print(f'Attempting to parse {email_file}...')
    time.sleep(0.5)
    email_request_type = email_file.removesuffix('_email.txt')
    with open(email_path, 'r') as email:
        email_msg = message_from_file(email, policy=policy.default)
        subject = email_msg['subject']
        email_from = email_msg['from']
        body = email_msg.get_body(('plain',)).get_content().strip("\n")
        parsed_subject = request_parser.parse_subject_universal(subject, email_from, body, helpdesk_dir, config)
        if email_request_type == 'unknown_request':
            request_type = parsed_subject['request_type']
            request_lookup = config['requests_directory'][request_type]
            assert request_lookup  == email_request_type, f"Failed to parse {email_file}. Parsed request type did not match {request_type}"
            print(f'Successfully parsed {email_file}')
            

        else:
            parsed_body = request_parser.parse_body_universal(parsed_subject)
            request = request_parser.execute_request_universal(parsed_body)
            assert 'request_type' in request and len(request.keys()) > 1, f'Failed to parse {email_file}. One or more of the required keys were not found in the test email.'
            print(f'Successfully parsed {email_file}')
