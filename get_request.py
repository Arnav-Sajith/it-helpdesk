#!/usr/bin/env python3
from sys import stdin 

with open("/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/user_request_email.log", "w") as itsupportrequest:
    for line in stdin:
        if line.rstrip() == 'Exit':
            break
        print(line.rstrip(), file=itsupportrequest)