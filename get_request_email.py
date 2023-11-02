from sys import stdin
import email
from email.policy import default
from email.utils import parseaddr
import parse_email as pe
from run_playbook import ansible_run




# def main():
#     email_msg = email.message_from_file(stdin, policy=default)
#     address = parseaddr(email_msg['from'])
#     address = address[1] if address[1] else address[0]
#     body = email_msg.get_body(('plain',)).get_content().strip("\n")


#     parsed_subject = pe.parse_subject_universal(email_msg['subject'], address, body)
#     parsed_body = pe.parse_body_universal(parsed_subject)
#     request_contents = pe.execute_request_universal(parsed_body)
#     request_contents['from'] = address
#     if not request_contents['valid_target']:
#         ansible_run(0, request_contents)
#     else:
#         ansible_run(request_contents['request_type'], request_contents)



def main():
    with open('sample.txt', 'r') as fp:
        email_msg = email.message_from_file(fp, policy=default)
        address = parseaddr(email_msg['from'])
        address = address[1] if address[1] else address[0]
        body = email_msg.get_body(('plain',)).get_content().strip("\n")


        parsed_subject = pe.parse_subject_universal(email_msg['subject'], address, body)
        parsed_body = pe.parse_body_universal(parsed_subject)
        print(parsed_body)
        request_contents = pe.execute_request_universal(parsed_body)
        request_contents['from'] = address
        # if not request_contents['valid_target']:
        #     ansible_run(0, request_contents)
        # else:
        #     ansible_run(request_contents['request_type'], request_contents)
    

    

if __name__ == '__main__':
    main()


