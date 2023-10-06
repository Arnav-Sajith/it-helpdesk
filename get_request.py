#!/usr/bin/env python3
from sys import stdin
import re
import unicodedata
important_headers =["From", "id", "To:", "Subject:", "Message-Id:", "Message-ID:", "References:", "Date:"] # need to fix for multiple references since each one is on a new line # also see if implementing isupper/islower is better 
headers_dictionary = {}
body = []
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
    for x in range(len(email_contents)):
        print(email_contents[x].strip(), file=email_log)

# From arnavsajith@arnav.local  Thu Oct  5 18:46:15 2023
# 	id 32E61D06B95; Thu,  5 Oct 2023 18:46:15 -0400 (EDT)
# From: arnavsajith@arnav.local
# To: arnavsajith@arnav.local
# Subject: New Employee
# Message-Id: <20231005224615.32E61D06B95@arnav.local>
# Date: Thu,  5 Oct 2023 18:46:15 -0400 (EDT)

# I have hired a new employee named John Walker. I'd like to create an account for him.




# From arnavsajith@arnav.local  Thu Oct  5 16:34:44 2023
# Return-Path: <arnavsajith@arnav.local>
# Received: by arnav.local (Postfix, from userid 501)
# 	id 9585DD03C56; Thu,  5 Oct 2023 16:34:44 -0400 (EDT)
# Date: Thu, 5 Oct 2023 16:34:44 -0400
# From: Arnav Sajith <arnav@arnav.local>
# To: arnavsajith@arnav.local
# Subject: Re: Test223
# Message-ID: <ZR8d5IIRvLq-9u_J@arnav>
# References: <ZR8H6lnbihx718Zh@arnav>
# MIME-Version: 1.0
# Content-Type: text/plain; charset=us-ascii
# Content-Disposition: inline
# In-Reply-To: <ZR8H6lnbihx718Zh@arnav>

# Please give me more money

# Return-Path: <arnavsajith@arnav.local>
# X-Original-To: arnavsajith@arnav.local
# Delivered-To: arnavsajith@arnav.local
# Received: by arnav.local (Postfix, from userid 501)
#         id E5953D01D2B; Thu,  5 Oct 2023 15:00:58 -0400 (EDT)
# Date: Thu, 5 Oct 2023 15:00:58 -0400
# From: Arnav Sajith <arnav@arnav.local>
# To: arnavsajith@arnav.local
# Subject: Test223
# Message-ID: <ZR8H6lnbihx718Zh@arnav>
# MIME-Version: 1.0
# Content-Type: text/plain; charset=us-ascii
# Content-Disposition: inline

# what do you want

  # if not email_contents[x].split(' ',maxsplit=1)[0] in important_headers:
            #     print(x, file=email_log)
            #     print(email_contents[x].rstrip(), file=email_log)ß
            #     x = x - 1
            #     print(x, file=email_log)
            
            # else:   
            #     print(email_contents[x].rstrip(), file=email_log)