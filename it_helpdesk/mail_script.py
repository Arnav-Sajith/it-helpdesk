from sys import stdin
import os
from email import policy, message_from_file
from it_helpdesk import get_request_email as gre
import yaml

def main():
    path = os.path.join(os.path.dirname(__file__), 'ansible/vars/it_helpdesk_config.yaml')
    with open(path) as config:
        message = message_from_file(stdin, policy=policy.default)
        # message = message_from_file(open(os.path.join(os.path.dirname(__file__),'ansible/sample_email.txt'), 'r'), policy=policy.default)
        gre.main(message, f'{yaml.safe_load(config)["helpdesk_dir"]}/ansible')

if __name__ == '__main__':
    main()