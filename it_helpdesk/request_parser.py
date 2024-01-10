#!/usr/bin/env python
import re
import shlex
import os
import yaml

def is_valid_amount(amount: str):
    if amount.isdigit():
        return int(amount)
    else:
        try:
            return float(amount)
        except(ValueError):
            return False
        
def load_phrases(phrasebook, ansible_dir):
    phrasebook_path = os.path.join(ansible_dir, 'phrasebooks', f'{phrasebook}.txt')
    with open(phrasebook_path, "r") as phrases:
        phrases_dict = {}
        key = None  # store the most recent "command" here
        for line in phrases.readlines():
            if line[0] == '*':
                key = line.strip("*\n") # your "command"
                phrases_dict[key] = []
            elif line[0] != '#':
                phrases_dict[key] = (shlex.split(line))
    return phrases_dict 

def get_request_type(subject_entered, ansible_dir):
    keywords = load_phrases(".keywords", ansible_dir)
    subject = subject_entered.lower()
    for request_type in keywords:
        if any(keyword in subject for keyword in keywords[request_type]):
            request_type_index = list(keywords.keys()).index(request_type) + 1
            return request_type_index
    return 0
        
def parse_subject_universal(subject_entered : str, email_from : str, body : str, helpdesk_dir : str, config: dict):
    ansible_dir = os.path.join(helpdesk_dir, 'ansible')
    request_type = get_request_type(subject_entered, ansible_dir)
    if request_type == 0:
        return {'request_type': request_type}
    requests_directory = config['requests_directory']
    subject = subject_entered.lower()
    subject_words = set(subject.split()) # Create a set of subject words, stopping substring matching and improving speed
    phrases = load_phrases(f"{requests_directory[request_type]}_phrases", ansible_dir)
    parse_subject_dict = {key: None for key in phrases.keys()}
    parse_subject_dict.update({'request_type': request_type, 'email': email_from, 'subject': subject_entered, 'body': body, 'phrases': phrases})
    for phrase in phrases:
        if any(keyword in subject_words for keyword in phrases[phrase]):
            parse_subject_dict[phrase] = True            
    return parse_subject_dict

def parse_body_universal(parsed_subject_dict: dict):    
    parse_body_dict = parsed_subject_dict
    body_words = parsed_subject_dict['body'].split()
    phrases = parsed_subject_dict['phrases']
    # get values that weren't in subject from body
    needed_values = {keyword for keyword in parse_body_dict if not parse_body_dict[keyword]}
    for phrase in needed_values:
        if any(keyword in body_words for keyword in phrases[phrase]) and phrase != 'targets':
            parse_body_dict[phrase] = True    

    if 'modifiers' in phrases:
            unit = phrases['unit'][0]
            modifiers = phrases['modifiers']
            pattern = fr'(\S+\s+\S+)\s*({unit})' # pulls the first gb and the two previous words (/S) separated by spaces (/s)
            matches = re.findall(pattern, parse_body_dict['body'], re.IGNORECASE)
            if matches and any((match := modifier) in matches[0][0] for modifier in modifiers) and is_valid_amount(matches[0][0].strip(match)):
                parse_body_dict["modifiers"] = match
                parse_body_dict['amount'] = matches[0][0].strip(f'{match} ')
                parse_body_dict['unit'] = unit

    # get target for request 
    if parse_body_dict['selftargets'] and not parse_body_dict['targets']:
        parse_body_dict['targets'] = parse_body_dict['email'].split("@")[0]

    while True:
        if any((match := target) in body_words for target in phrases['targets']): # add more options for default and for multiple users
            if not parse_body_dict['targets']:
                target_index = body_words.index(match)
                username = body_words[target_index + 1]
                parse_body_dict['targets'] = username.split("@")[0] #if is_valid_target(username, parse_body_dict) else None
                del body_words[target_index]
            else:
                target_index = body_words.index(match)
                target_value = body_words[target_index + 1]
                parse_body_dict[match.strip(':')] = target_value
                del body_words[target_index]
        else:
            if any(self_target in body_words for self_target in phrases["selftargets"]):
                parse_body_dict['targets'] = parse_body_dict['email'].split("@")[0]
                parse_body_dict['selftargets'] = True
            break

    del parse_body_dict['phrases'], parse_body_dict['email'], parse_body_dict['selftargets'], parse_body_dict['body']
    return parse_body_dict

def execute_request_universal(parsed_body_dict: dict):
    return parsed_body_dict
 
