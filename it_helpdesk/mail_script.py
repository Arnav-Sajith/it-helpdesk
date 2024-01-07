from sys import stdin
from email import policy, message_from_file
from it_helpdesk import get_request_email as gre
import yaml

def main():
    with open('ansible/vars/it_helpdesk_config.yaml') as config:
        gre.main(message_from_file(stdin, policy=policy.default), f'{yaml.safe_load(config)["helpdesk_dir"]}/ansible')

if __name__ == '__main__':
    main()