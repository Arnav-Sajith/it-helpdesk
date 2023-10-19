# Import the email modules we'll need
from sys import stdin
import email
from email.parser import BytesParser
# trunk-ignore(ruff/F401)
from email.parser import Parser
from email.policy import default
from email.utils import parseaddr
import parse_email as pe
import ansible_runner
from pyisemail import is_email

important_headers =["from", "id", "to", "subject", "message-id:", "references", "date:"] # need to fix for multiple references since each one is on a new line # also see if implementing isupper/islower is better 

with open("/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/user_request_email.log", "w") as email_log:
    email_msg = email.message_from_file(stdin, policy=default)
    address = parseaddr(email_msg['from'])
    address = address[1] if address[1] else address[0]
    body = email_msg.get_body(('plain',))
    if body:
        body = body.get_content().strip("\n")
    print(body, file=email_log)
    print(email_msg, file=email_log)
    print("\n\n\n\n", file=email_log)
    print(email_msg['subject'], file=email_log)
    print(address, file=email_log)
    print(body, file=email_log)
    print("\n\n\n\n", file=email_log)
    # with open("approved_commands.txt", "r") as approved_commands:  
    #     body = body.split()
    #     for word in body:
    #         if word not in approved_commands.read():
    #             print("Illegal input detected", file=email_log)
    #         else:
    #             shell_request = {'body': body[0], 'from': address, 'date': email_msg['date'].replace(" ", "_").replace(":", "_")}
    #             print(shell_request, file=email_log)
    #             runner_config = ansible_runner.config.runner.RunnerConfig(private_data_dir="/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk", playbook="/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/email_shell.yaml", inventory = "/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/inventory.yaml", extravars = shell_request)
    #             runner_config.prepare()
    #             rc = ansible_runner.runner.Runner(config=runner_config)
                # rc.run()

    parsed_subject = pe.parse_subject(email_msg['subject'], address, body)
    print(parsed_subject, file=email_log)
    storage_request_contents = pe.execute_request(parsed_subject)
    storage_request_contents['date'] = email_msg['date'].replace(" ", "_").replace(":", "_")
    storage_request_contents['from'] = address
    print(storage_request_contents, file=email_log)
    runner_config = ansible_runner.config.runner.RunnerConfig(private_data_dir="/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk", playbook="/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/increase_storage.yaml", inventory = "/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/inventory.yaml", extravars = storage_request_contents)
    runner_config.prepare()
    rc = ansible_runner.runner.Runner(config=runner_config)
    rc.run()