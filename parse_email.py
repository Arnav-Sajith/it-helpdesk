#!/usr/bin/env python
import re
import shlex
from pyisemail import is_email
import time

# for reference
request_type_lookup = {1: 'storage', 
                       2: 'manage_account', 
                       3: 'query_account',
                       4: 'management'}

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
        
def load_phrases(phrasebook): # implement universal phrases with targets and self-targets
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
    parse_subject_dict.update({'request_type': request_type, 'email': email_from, 'body': body, 'phrases': phrases})
    for phrase in phrases:
        if any(keyword in subject_words for keyword in phrases[phrase]):
            parse_subject_dict[phrase] = True            
    return parse_subject_dict

parsed_subject = parse_subject_universal("Increase storage request", "arnavsajith04@gmail.com", "Hello, please increase my storage quota by 1.2gb")
# parsed_subject = parse_subject_universal("Storage query", "arnavsajith04@gmail.com", "How much storage do I have left")
# parsed_subject = parse_subject_universal("Change username", "arnavsajith04@gmail.com", "Hello, I'd like to change my username")

def parse_body_universal(parsed_subject_dict: dict):
    parse_body_dict = parsed_subject_dict
    body_words = parsed_subject_dict['body'].split()
    phrases = parsed_subject_dict['phrases']

    # get values that weren't in subject from body
    needed_values = {keyword for keyword in parse_body_dict if not parse_body_dict[keyword]}
    for phrase in needed_values:
        if any(keyword in body_words for keyword in phrases[phrase]):
            parse_body_dict[phrase] = True       

    # get target for request 
    if parse_body_dict['selftargets'] and not parse_body_dict['targets']:
        parse_body_dict['targets'] = parse_body_dict['email'].split("@")[0]

    elif any((match := target) in body_words for target in phrases['targets']): # add more options for default and for multiple users
        target_index = body_words.index(match)
        username = body_words[target_index + 1]
        parse_body_dict['targets'] = "default user" if match == "default" else username.split("@")[0] if is_valid_target(username) else None
    else:
        if any(self_target in body_words for self_target in phrases["selftargets"]):
            parse_body_dict['targets'] = parse_body_dict['email'].split("@")[0]
            parse_body_dict['selftargets'] = True
        
    if 'modifiers' in phrases:
        unit = phrases['unit'][0]
        modifiers = phrases['modifiers']
        pattern = fr'(\S+\s+\S+)\s*({unit})' # pulls the first gb and the two previous words (/S) separated by spaces (/s)
        matches = re.findall(pattern, parse_body_dict['body'], re.IGNORECASE)
        if matches and any((match := modifier) in matches[0][0] for modifier in modifiers) and is_valid_amount(matches[0][0].strip(match)):
            parse_body_dict["modifiers"] = match
            parse_body_dict['amount'] = matches[0][0].strip(f'{match} ')
            parse_body_dict['unit'] = unit
    
    
    del parse_body_dict['phrases'], parse_body_dict['email'], parse_body_dict['body'], parse_body_dict['selftargets']
    print(parse_body_dict)
    return parse_body_dict

parse_body_universal(parsed_subject)

def execute_request_universal(parsed_body_dict: dict):
    if not parsed_body_dict['targets']:
        request_contents = {}
        request_contents['valid_target'] = False
        return request_contents
    else:
        request_contents = parsed_body_dict
        request_contents['valid_target'] = True
        return request_contents

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
        if matches and any((match := modifier) in matches[0][0] for modifier in modifiers) and is_valid_amount(matches[0][0].strip(match)):
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

# print(parse_body(True, "Hello, I'd like to know how much storage user alice has left", False))
    
def execute_request(parse_subject_dict : dict):
    if parse_subject_dict['request_type'] == 1:
        storage_request_contents = parse_body(parse_subject_dict['target_not_sender'], parse_subject_dict['body'], parse_subject_dict['query'])
        storage_request_contents['target'] = parse_subject_dict['email'] if storage_request_contents['target'] is None else storage_request_contents['target']
        storage_request_contents['valid_target'] = is_valid_target(storage_request_contents['target'])
        storage_request_contents['positive_action'] = parse_subject_dict['positive_verb']
        storage_request_contents['query'] = parse_subject_dict['query']
        return storage_request_contents
