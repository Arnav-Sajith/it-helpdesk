import it_helpdesk
import os
import time
from it_helpdesk import request_parser, get_request_email as gre
from email import message_from_file, policy

def test_parse_subject():
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
            subject = email_msg['subject']
            email_from = email_msg['from']
            body = email_msg.get_body(('plain',)).get_content().strip("\n")
            parsed_subject = request_parser.parse_subject_universal(subject, email_from, body, helpdesk_dir, config)
            if email_request_type == 'unknown_request':
                request_type = parsed_subject['request_type']
                request_lookup = config['requests_directory'][request_type]
                assert request_lookup  == email_request_type
                print(f'Successfully parsed {email_file}')
                

            else:
                parsed_body = request_parser.parse_body_universal(parsed_subject)
                request = request_parser.execute_request_universal(parsed_body)
                assert 'request_type' in request
                assert len(request.keys()) > 1
                print(f'Successfully parsed {email_file}')
        time.sleep(1)

    print('Successfully parsed all test emails')
test_parse_subject()