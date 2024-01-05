from sys import stdin
import email
import request_parser
from email.policy import default
from email.utils import parseaddr
from ansible_runner.config.runner import RunnerConfig
from ansible_runner.runner import Runner



def ansible_run(request_type : int, request_contents : dict):
    requests = {0: 'invalid_request',
                1: 'storage', 
                2: 'manage_account', 
                3: 'query_account',
                4: 'manage_users',
                5: 'help'}
    runner_config = RunnerConfig(private_data_dir ="./ansible", inventory="./inventory", playbook=f"/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/{requests[request_type]}.yaml", extravars = request_contents)
    runner_config.prepare()
    rc = Runner(config=runner_config)
    rc.run()

def main():
    email_msg = email.message_from_file(stdin, policy=default)
    address = parseaddr(email_msg['from'])[1] if parseaddr(email_msg['from'])[1] else parseaddr(email_msg['from'])[0]
    body = email_msg.get_body(('plain',)).get_content().strip("\n")
    parsed_subject = request_parser.parse_subject_universal(email_msg['subject'], address, body)
    parsed_body = request_parser.parse_body_universal(parsed_subject)
    request = {**request_parser.execute_request_universal(parsed_body), 'from': address}
    ansible_run(request['request_type'], request)
    

if __name__ == '__main__':
    main()