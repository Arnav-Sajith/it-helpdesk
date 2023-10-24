from sys import stdin
import email
from email.policy import default
from email.utils import parseaddr
import parse_email as pe
from run_playbook import ansible_run




def main():
    email_msg = email.message_from_file(stdin, policy=default)
    address = parseaddr(email_msg['from'])
    address = address[1] if address[1] else address[0]
    body = email_msg.get_body(('plain',)).get_content().strip("\n")


    parsed_subject = pe.parse_subject_universal(email_msg['subject'], address, body)
    parsed_body = pe.parse_body_universal(parsed_subject)
    request_contents = pe.execute_request_universal(parsed_body)
    request_contents['from'] = address
    if not request_contents['valid_target']:
        valid_target = False
        ansible_run(0, request_contents)
    else:
        request_type = request_contents['request_type']
        ansible_run(request_type, request_contents)
    # parsed_subject = pe.parse_subject(email_msg['subject'], address, body)
    # request_type = parsed_subject['request_type']
    # storage_request_contents = pe.execute_request(parsed_subject)
    # storage_request_contents['from'] = address
    # ansible_run(request_type, storage_request_contents)
  

    

if __name__ == '__main__':
    main()


