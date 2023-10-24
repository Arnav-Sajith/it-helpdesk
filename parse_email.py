#!/usr/bin/env python
import re
import shlex
from pyisemail import is_email
import time

# for reference
request_type_lookup = {1: 'storage', 
                       2: 'account', 
                       3: 'management'}

def is_valid_amount(amount: str):
    if amount.isdigit():
        return int(amount)
    else:
        try:
            return float(amount)
        except(ValueError):
            return False
        
def is_valid_target(target : str):
    with open("existing_users.txt", 'r') as existing_users:
        target = target.split("@")[0]
        return True if target+'\n' in existing_users else False
        
def load_phrases(phrasebook):
    with open(f"{phrasebook}.txt", "r") as phrases:
        phrases_dict = {}
        key = None  # store the most recent "command" here
        for line in phrases.readlines():
            if line[0] == '*':
                key = line.strip("*\n") # your "command"
                phrases_dict[key] = []
            elif line[0] != '#':
                phrases_dict[key] = (shlex.split(line))
    return phrases_dict

def get_request_type(subject_entered):
    keywords = load_phrases("keywords")
    subject = subject_entered.lower()
    count = 1
    for request_type in keywords:
        if any(keyword in subject for keyword in keywords[request_type]):
            return count
        count += 1

def parse_subject_universal(subject_entered : str, email_from : str, body : str):
    subject = subject_entered.lower()
    request_type = get_request_type(subject)
    
    subject_words = set(subject.split()) # Create a set of subject words, stopping substring matching and improving speed
    phrases = load_phrases(f"{request_type_lookup[request_type]}_phrases")
    parse_subject_dict = {key: None for key in phrases.keys()}
    parse_subject_dict.update({'request_type': request_type, 'email': email_from, 'body': body})
    for phrase in phrases:
        if any(keyword in subject_words for keyword in phrases[phrase]):
            parse_subject_dict[phrase] = True
            
    print(parse_subject_dict)
    return parse_subject_dict
parse_subject_universal("Increase storage request", "arnavsajith04@gmail.com", "Hello, please increase the storage quota for user: jacob by 1.2gb")
# parse_subject_universal("What is my account username", "arnavsajith04@gmail.com", "Please tell me what the username for my account is")

def parse_body_universal(parsed_subject_dict: dict):
    

def parse_subject(subject_entered : str, email_from : str, body : str):
    subject = subject_entered.lower()
    request_type = get_request_type(subject)
    if request_type == 1:
        storage_phrases = load_phrases("storage_phrases")
        parse_subject_dict = {'request_type': 1, 'query': None, 'positive_verb': None, 'negative_verb': None, 'target_not_sender': None, 'valid_request': None, 'email': email_from, 'body': body}
        if any(query in subject for query in storage_phrases["queries"]):
            parse_subject_dict['query'] = True
        if any(positive_verb in subject for positive_verb in storage_phrases["verbs_positive"]):
            parse_subject_dict['positive_verb'] = True
        if any(negative_verb in subject for negative_verb in storage_phrases["verbs_negative"]):
            parse_subject_dict['negative_verb'] = True
        if any(target in subject for target in storage_phrases["targets"]) and not any(self_target in subject for self_target in storage_phrases["selftargets"]):
            parse_subject_dict['target_not_sender'] = True
        # if (positive_verb and negative_verb):
        #     print("Sorry, I couldn't comprehend your request. The subject contains both a positive: '", positive_verb, "' and a negative '", negative_verb, "'")
        #     valid_request = False
        #     return valid_request
        return parse_subject_dict
print(parse_subject('Increase storage request', 'arnavsajith04@gmail.com', 'Hello, please increase the storage quota for user: jacob by 1.2gb'))

def parse_body(target_not_sender: bool, body: str, query: bool):
    body_words = body.split()
    amount = {"modifier": None, "amount": None, "unit": None, "target": None}
    storage_phrases = load_phrases("storage_phrases")
    modifiers = storage_phrases["modifiers"]
    targets = storage_phrases["targets"]
    unit = storage_phrases['unit'][0]
    if not query: 
        pattern = fr'(\S+\s+\S+)\s*({unit})' # pulls the first gb and the two previous words (/S) separated by spaces (/s)
        matches = re.findall(pattern, body, re.IGNORECASE)
        if any((match := modifier) in matches[0][0] for modifier in modifiers) and is_valid_amount(matches[0][0].strip(match)):
                    amount["modifier"] = match
                    amount['amount'] = matches[0][0].strip(f'{match} ')
                    amount['unit'] = matches[0][1]
    
    if any((match := target) in body_words for target in targets): # add more options for default and for multiple users
        target_index = body_words.index(match)
        username = body_words[target_index + 1]
        amount['target'] = "default user" if match == "default" else username

    elif amount['target'] is None:
        for target in body_words:
                amount['target'] = target if is_email(target) else None

    elif not target_not_sender:
        amount['target'] = None
    return amount
    
    # else: 
    #     with open('existing_users', 'r') as existing_users:  #TODO create matching for all emails if user exists
    #         if any((match := user) in body_words for user in existing_users):
    #             amount['target'] = match
    #         else:
                
    #         return amount

parse_body(True, 'Hello, please increase the storage quota for user: jacob by 1.2gb', False)
    
def execute_request(parse_subject_dict : dict):
    if parse_subject_dict['request_type'] == 1:
        storage_request_contents = parse_body(parse_subject_dict['target_not_sender'], parse_subject_dict['body'], parse_subject_dict['query'])
        storage_request_contents['target'] = parse_subject_dict['email'] if storage_request_contents['target'] is None else storage_request_contents['target']
        storage_request_contents['valid_target'] = is_valid_target(storage_request_contents['target'])
        storage_request_contents['positive_action'] = parse_subject_dict['positive_verb']
        storage_request_contents['query'] = parse_subject_dict['query']
        return storage_request_contents
