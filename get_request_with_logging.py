#!/usr/bin/env python3
from sys import stdin
import re
import unicodedata
important_headers =["From", "id", "To:", "Subject:", "Message-Id:", "Message-ID:", "References:", "Date:"] # need to fix for multiple references since each one is on a new line # also see if implementing isupper/islower is better 
headers_dictionary = {}
unimportant_headers = []
email_contents = []


def clean_value_header(header, email_content_line):
    value_clean = re.sub(f'{header}', '', email_content_line)
    value_clean = re.sub('[<,;>]', '', value_clean)
    value_clean = value_clean.strip()
    header_clean = header.lower().strip(":")
    if header_clean == "date" or header_clean == 'subject':
        return value_clean, header_clean
    else:
        return value_clean.split()[0], header_clean.lstrip()

def add_to_dict(clean_header, clean_value):
    headers_dictionary[f'{clean_header}'] = f'{clean_value}'
    return headers_dictionary



with open("/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/user_request_email.log", "w") as email_log:
    for line in stdin:
        print(line.strip(), file=email_log)
        email_contents.append(line)
    print("\n\n", file=email_log)
    lines_of_email = len(email_contents)
    try:
        x = 0
        while x <= lines_of_email:
            if email_contents[x] == "\n":
                del(email_contents[x])
                body = ''.join(email_contents[x:])
                print(add_to_dict("body", body), file=email_log)
                break
            header = email_contents[x].split(maxsplit=1)[0]    
            if header not in important_headers:
                unimportant_headers.append(email_contents[x])
                del(email_contents[x])
                x -= 1
            else:
                print(email_contents[x].strip(), file=email_log)
                clean_value, clean_header = clean_value_header(header, email_contents[x])
                print(clean_value, "", clean_header, file=email_log)
                print(add_to_dict(clean_header, clean_value), file=email_log)
                
            x += 1   
    except(IndexError):
        print("x is equal to ", x, file=email_log)
        print(email_contents[-1], file=email_log)
        print(len(email_contents), file=email_log)

    print("\n\n\n\n", file=email_log)
    print(headers_dictionary)
    for x in range(len(email_contents)):
        print(email_contents[x].strip(), file=email_log)
