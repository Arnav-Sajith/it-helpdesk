#!/usr/bin/env python3
from sys import stdin
import re
import parse_email as pe
import ansible_runner

important_headers =["From", "id", "To:", "Subject:", "Message-Id:", "Message-ID:", "References:", "Date:"] # need to fix for multiple references since each one is on a new line # also see if implementing isupper/islower is better 
headers_dictionary = {}
unimportant_headers = []
email_contents = []


def clean_value_header(header: str, email_content_line: str):
    value_clean = re.sub(f'{header}', '', email_content_line)
    value_clean = re.sub('[<,;>]', '', value_clean)
    value_clean = value_clean.strip()
    header_clean = header.lower().strip(":")
    if header_clean == "date" or header_clean == 'subject':
        return value_clean, header_clean
    else:
        return value_clean.split()[0], header_clean.lstrip()

def add_to_dict(clean_header: str, clean_value: str):
    headers_dictionary[f'{clean_header}'] = f'{clean_value}'
    return headers_dictionary



with open("/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/user_request_email.log", "w") as email_log:
    for line in stdin:
        print(line.strip(), file=email_log)
        email_contents.append(line)
    print("\n\n", file=email_log)
    x = 0
    while x <= len(email_contents):
        if email_contents[x] == "\n":
            del(email_contents[x])
            body = ''.join(email_contents[x:])
            add_to_dict("body", body)
            break
        header = email_contents[x].split(maxsplit=1)[0]
        if header not in important_headers:
            unimportant_headers.append(email_contents[x])
            del(email_contents[x])
            x -= 1
        else:
            clean_value, clean_header = clean_value_header(header, email_contents[x])
            add_to_dict(clean_header, clean_value)
            
        x += 1   


    for header in headers_dictionary:
        print(header, ": ", headers_dictionary[header], file=email_log)
    
    parsed_subject = pe.parse_subject(headers_dictionary)
    storage_request_contents = pe.execute_request(*parsed_subject)
    storage_request_contents['date'] = headers_dictionary['date'].replace(" ", "_").replace(":", "_")
    print(storage_request_contents, file=email_log)
    runner_config = ansible_runner.config.runner.RunnerConfig(private_data_dir="/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk", playbook="/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/increase_storage.yaml", inventory = "/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/inventory.yaml", extravars = storage_request_contents)
    runner_config.prepare()
    rc = ansible_runner.runner.Runner(config=runner_config)
    rc.run()