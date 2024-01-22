from sys import stdin
import os
from email import policy, message_from_file
from it_helpdesk import get_request_email as gre
import yaml

def main():
    file_path = os.path.dirname(__file__)
    path = os.path.join(file_path, 'ansible', 'vars', 'it_helpdesk_config.yaml')
    with open(path) as config_file:
        config = yaml.safe_load(config_file)
        message = message_from_file(stdin, policy=policy.default)
        gre.main(message, config["helpdesk_dir"])

if __name__ == '__main__':
    main()